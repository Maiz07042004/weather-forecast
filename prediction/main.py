from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import os

from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresPredictionRepository
from app.infrastructure.modelAI.sklern_adapter import SklearnModelAdapter
from app.usecase.tempPrediction import PredictionService
from app.domain.model import PredictionResult

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")
DB_NAME = os.getenv("DB_NAME", "weather_db")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LAT = 51.5074
LON = -0.1278

MODEL_PATH = "app/infrastructure/models/Training_model_focast_temp.pkl"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine) 

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db),MODEL_PATH = MODEL_PATH):
    model_adapter = SklearnModelAdapter(MODEL_PATH)
    repo = PostgresPredictionRepository(db)
    return PredictionService(repo, model_adapter)

def run_prediction_job():
    db = SessionLocal()
    try:
        service = get_service(db, MODEL_PATH)
        service.predict_next_day()
    except Exception as e:
        print(f"Prediction Job Failed: {e}")
    finally:
        db.close()

# Lifecycle & Scheduler
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(">>> Starting Prediction Scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_prediction_job, 'interval', minutes=5)
    scheduler.start()
    
    run_prediction_job()
    
    yield
    print(">>> Stopping Prediction Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/predict/next-day", response_model=None)
def predict_weather(service: PredictionService = Depends(get_service)):
    try:
        result = service.predict_next_day()
        return {
            "forecast_date": result.forecast_date,
            "predicted_temp": result.predicted_temp,
            "based_on": result.based_on_last_date,
            "info": f"Predicted using {len(result.features_used)} features over 7 days"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)