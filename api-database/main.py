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
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_service(db: Session = Depends(get_db)):
    repo = WeatherRepository(db)
    return DashboardService(repo)

app = FastAPI(title="Weather Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 1: Lấy toàn bộ dữ liệu vẽ biểu đồ (Line/Scatter/Trend/Seasonal)
@app.get("/api/dashboard/charts")
def get_charts(days: int = 360, service: DashboardService = Depends(get_service)):
    """
    Trả về 3 bộ dữ liệu:
    - daily_series: Để vẽ Line, Scatter, Histogram chi tiết ngày.
    - weekly_series: Để vẽ Trend tuần.
    - monthly_series: Để vẽ Trend tháng & Seasonal line.
    """
    return service.get_charts_data(daily_limit=days)

# API 2: Lấy ma trận Correlation (Vẽ Heatmap)
@app.get("/api/dashboard/correlation")
def get_correlation(service: DashboardService = Depends(get_service)):
    return service.get_correlation()

# API 3: Lấy dự báo ngày mai (Temp + Weather Type)
@app.get("/api/dashboard/forecast")
def get_forecast(service: DashboardService = Depends(get_service)):
    data = service.get_forecast()
    if not data:
        return {"status": "No forecast available"}
    return data

# @app.get("/api/dashboard/charts/resample")
# def get_resampled_charts(granularity: str = 'M', limit: int = 12, service: DashboardService = Depends(get_service)):
#     """
#     Lấy dữ liệu đã được resample theo chu kỳ (M: Monthly, W: Weekly)
#     Dùng để vẽ Line Chart/Seasonal Chart với độ mượt cao hơn.
#     """
#     return service.(granularity=granularity, limit=limit)
if __name__ == "__main__":
    import uvicorn
    # Chạy port 8004
    uvicorn.run(app, host="0.0.0.0", port=8004)