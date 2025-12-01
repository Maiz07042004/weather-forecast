from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os

from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import WeatherRepository
from app.usecase.dashboardService import DashboardService

# 1. Cấu hình
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

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db)):
    repo = WeatherRepository(db)
    return DashboardService(repo)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard/charts")
def get_charts(days: int = 360, service: DashboardService = Depends(get_service)):
    return service.get_charts_data(daily_limit=days)

@app.get("/api/dashboard/correlation")
def get_correlation(service: DashboardService = Depends(get_service)):
    return service.get_correlation()

@app.get("/api/dashboard/forecast")
def get_forecast(service: DashboardService = Depends(get_service)):
    data = service.get_forecast()
    if not data:
        return {"status": "No forecast available"}
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)