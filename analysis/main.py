from fastapi import FastAPI, BackgroundTasks, Depends
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Import theo cấu trúc Hexagonal mới
from app.infrastructure.database.orm import Base, WeatherAggregateORM, CorrelationORM
from app.infrastructure.database.postgres_repo import PostgresAnalysisRepository
from app.usecase.analysis import AnalysisService

# 1. Config
load_dotenv()
# Dùng chung DB với Ingestion Service
DB_URL = os.getenv("DB_URL", "postgresql://postgres:12345@localhost:5432/weather_db")

# 2. Database Setup
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine) # Tạo bảng Aggregates & Correlation

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# 3. Dependency Injection Helper
def run_analysis_job():
    db = SessionLocal()
    try:
        # Lắp ráp: DB Session -> Repo Impl -> UseCase
        repo = PostgresAnalysisRepository(db)
        service = AnalysisService(repo)
        service.run_analysis()
    except Exception as e:
        print(f"Analysis Job Failed: {e}")
    finally:
        db.close()

# 4. Lifecycle & Scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting Analysis Scheduler...")
    scheduler = BackgroundScheduler()
    # Chạy mỗi 1 giờ
    scheduler.add_job(run_analysis_job, 'interval', hours=1)
    scheduler.start()
    
    # Chạy 1 lần lúc khởi động
    run_analysis_job()
    
    yield
    print(">>> Stopping Analysis Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan, title="Weather Analysis Service (Hexagonal)")

# 5. API Endpoints (Phục vụ Frontend)

@app.post("/trigger")
def trigger_analysis(background_tasks: BackgroundTasks):
    """Kích hoạt chạy phân tích thủ công"""
    background_tasks.add_task(run_analysis_job)
    return {"message": "Analysis triggered in background"}

@app.get("/charts/aggregates")
def get_aggregates(granularity: str = 'M', limit: int = 12, db: Session = Depends(get_db)):
    """Lấy dữ liệu vẽ Line Chart/Seasonal"""
    data = db.query(WeatherAggregateORM)\
             .filter(WeatherAggregateORM.granularity == granularity)\
             .order_by(WeatherAggregateORM.date.desc())\
             .limit(limit).all()
    return data[::-1]

@app.get("/charts/correlation")
def get_correlation(db: Session = Depends(get_db)):
    """Lấy dữ liệu vẽ Heatmap"""
    record = db.query(CorrelationORM).order_by(CorrelationORM.id.desc()).first()
    return record.matrix if record else {}

if __name__ == "__main__":
    import uvicorn
    # Chạy ở port khác với Ingestion
    uvicorn.run(app, host="0.0.0.0", port=8001)