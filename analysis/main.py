from fastapi import FastAPI, BackgroundTasks, Depends
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

from app.infrastructure.database.orm import Base, WeatherAggregateORM, CorrelationORM
from app.infrastructure.database.postgres_repo import PostgresAnalysisRepository
from app.usecase.analysis import AnalysisService

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_NAME = os.getenv("DB_NAME", "weather_db")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LAT = 51.5074
LON = -0.1278

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def run_analysis_job():
    db = SessionLocal()
    try:
        repo = PostgresAnalysisRepository(db)
        service = AnalysisService(repo)
        service.run_analysis()
    except Exception as e:
        print(f"Analysis Job Failed: {e}")
    finally:
        db.close()

# Lifecycle & Scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting Analysis Scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_analysis_job, 'interval', minutes=5)
    scheduler.start()
    
    run_analysis_job()
    
    yield
    print(">>> Stopping Analysis Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/trigger")
def trigger_analysis(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_analysis_job)
    return {"message": "Analysis triggered in background"}

@app.get("/charts/aggregates")
def get_aggregates(granularity: str = 'M', limit: int = 12, db: Session = Depends(get_db)):
    try:
        data = db.query(WeatherAggregateORM)\
                 .filter(WeatherAggregateORM.granularity == granularity)\
                 .order_by(WeatherAggregateORM.date.desc())\
                 .limit(limit).all()
        return data[::-1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/charts/correlation")
def get_correlation(db: Session = Depends(get_db)):
    record = db.query(CorrelationORM).order_by(CorrelationORM.id.desc()).first()
    return record.matrix if record else {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)