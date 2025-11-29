from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

# Import Components
from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresClusteringRepository
from app.infrastructure.modelAI.sklearn_adapter import SklearnClassifierAdapter
from app.usecase.weatherClustering import ClusteringService

# 1. Config
load_dotenv()
DB_URL = os.getenv("DB_URL", "postgresql://postgres:12345@localhost:5432/weather_db")
MODEL_PATH = "app/infrastructure/models/Training_model_focast_weather_code.pkl"

# 2. Setup
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
# Tạo bảng weather_clusters
Base.metadata.create_all(bind=engine)

# 3. Dependency Injection
model_adapter = SklearnClassifierAdapter(MODEL_PATH)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db)):
    repo = PostgresClusteringRepository(db)
    return ClusteringService(repo, model_adapter)

app = FastAPI(title="Weather Clustering Service (Hexagonal)")

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