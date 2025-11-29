from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresPredictionRepository
from app.infrastructure.modelAI.sklern_adapter import SklearnModelAdapter
from app.usecase.tempPrediction import PredictionService
from app.domain.model import PredictionResult

# 1. Config
load_dotenv()
DB_URL = os.getenv("DB_URL", "postgresql://postgres:12345@localhost:5432/weather_db")
MODEL_PATH = "app/infrastructure/models/Training_model_focast_temp.pkl"

# 2. Setup
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)

# [QUAN TRỌNG] Bỏ comment dòng này để tạo bảng 'weather_predictions' mới
Base.metadata.create_all(bind=engine) 

# 3. Dependency Injection
# Khởi tạo Model Adapter 1 lần duy nhất (Singleton) khi start app
model_adapter = SklearnModelAdapter(MODEL_PATH)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db)):
    repo = PostgresPredictionRepository(db)
    # Tiêm Model Adapter và Repo vào Service
    return PredictionService(repo, model_adapter)

app = FastAPI(title="Weather Prediction Service (Hexagonal)")

@app.get("/predict/next-day", response_model=None)
def predict_weather(service: PredictionService = Depends(get_service)):
    try:
        result = service.predict_next_day()
        # Trả về Dict hoặc Object tùy ý
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
    # Chạy port 8002 để không đụng Ingestion(8000) và Analysis(8001)
    uvicorn.run(app, host="0.0.0.0", port=8002)