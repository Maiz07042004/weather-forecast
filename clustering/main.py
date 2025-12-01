from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresClusteringRepository
from app.infrastructure.modelAI.sklearn_adapter import SklearnClassifierAdapter
from app.usecase.weatherClustering import ClusteringService

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

MODEL_PATH = "app/infrastructure/models/Training_model_focast_weather_code.pkl"

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db),MODEL_PATH = MODEL_PATH):
    model_adapter = SklearnClassifierAdapter(MODEL_PATH)
    repo = PostgresClusteringRepository(db)
    return ClusteringService(repo, model_adapter)

def run_clustering_job():
    db = SessionLocal()
    try:
        service = get_service(db, MODEL_PATH)
        service.predict_weather_type()
    except Exception as e:
        print(f"Clustering Job Failed: {e}")
    finally:
        db.close()

# Lifecycle & Scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting Clustering Scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_clustering_job, 'interval', minutes=5)
    scheduler.start()
    
    run_clustering_job()
    
    yield
    print(">>> Stopping Clustering Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/predict/weather-type")
def predict_weather_type(service: ClusteringService = Depends(get_service)):
    try:
        result = service.predict_weather_type()
        return {
            "date": result.forecast_date,
            "weather_code": result.predicted_weather_code,
            "info": "Prediction based on latest daily data"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)