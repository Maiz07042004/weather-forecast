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