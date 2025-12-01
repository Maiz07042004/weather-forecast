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

# 1. Cấu hình
load_dotenv()

# CẤU HÌNH POSTGRESQL
# Định dạng: postgresql://username:password@host:port/database_name
# Cấu hình các tham số kết nối
DB_HOST = os.getenv("DB_HOST", "localhost")  # Lấy từ biến môi trường hoặc dùng localhost
DB_PORT = os.getenv("DB_PORT", 5432)  # Mặc định là 5432 cho PostgreSQL
DB_USER = os.getenv("DB_USER", "postgres")  # Người dùng (user)
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345")  # Mật khẩu (password)
DB_NAME = os.getenv("DB_NAME", "weather_db")  # Tên cơ sở dữ liệu

# Tạo URL kết nối theo từng phần
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

LAT = 51.5074  # London
LON = -0.1278

# 2. Setup Database Engine
engine = create_engine(DB_URL)

MODEL_PATH = "app/infrastructure/models/Training_model_focast_weather_code.pkl"

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