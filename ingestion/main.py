from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import os
from dotenv import load_dotenv

# Import các lớp từ các tầng Hexagonal
from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresRepository
from app.infrastructure.openmeteo.client import OpenMeteoClient
from app.usecase.ingestion import WeatherIngestionService

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
Base.metadata.create_all(bind=engine) # Tạo bảng nếu chưa có

# 3. Dependency Injection Factory
# Hàm này giúp tạo ra một instance Service hoàn chỉnh với đầy đủ phụ tùng
def get_ingestion_service(db_session):
    repo = PostgresRepository(session=db_session)
    client = OpenMeteoClient(lat=LAT, lon=LON)
    service = WeatherIngestionService(api_client=client, repo=repo)
    return service

# 4. Định nghĩa Job cho Scheduler
def job_ingestion_5min():
    """
    Job chạy ngầm: Tự động lấy dữ liệu 7 ngày gần nhất.
    Lý do lấy 7 ngày: Dữ liệu Daily Archive thường có độ trễ vài ngày
    hoặc được hiệu chỉnh lại, nên lấy gối đầu để luôn chính xác.
    """
    print("--- [CRON] Bắt đầu Job Ingestion định kỳ ---")
    db = SessionLocal()
    try:
        service = get_ingestion_service(db)
        
        # Lấy từ 7 ngày trước đến hôm nay
        end_d = date.today()
        start_d = end_d - timedelta(days=7)
        
        service.execute(
            start_date=start_d.strftime("%Y-%m-%d"),
            end_date=end_d.strftime("%Y-%m-%d")
        )
    except Exception as e:
        print(f"--- [CRON ERROR] {e}")
    finally:
        db.close() # Rất quan trọng: Phải đóng session sau khi chạy job

# 5. Cấu hình FastAPI & Scheduler Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print(">>> Khởi động Scheduler...")
    scheduler = BackgroundScheduler()
    
    # Thêm job chạy mỗi 5 phút
    scheduler.add_job(job_ingestion_5min, 'interval', minutes=5)
    scheduler.start()
    
    # Chạy ngay 1 lần khi khởi động để không phải chờ 5p
    job_ingestion_5min()
    
    yield
    
    # --- SHUTDOWN ---
    print(">>> Dừng Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# 6. API Endpoint (Để test hoặc kích hoạt thủ công)
@app.post("/ingest/manual")
def manual_ingest(start_date: str, end_date: str, background_tasks: BackgroundTasks):
    """
    API kích hoạt Ingestion thủ công.
    Dùng BackgroundTasks để không block request nếu thời gian lấy lâu.
    """
    def task():
        db = SessionLocal()
        try:
            service = get_ingestion_service(db)
            service.execute(start_date, end_date)
        finally:
            db.close()

    background_tasks.add_task(task)
    return {"message": f"Đã nhận lệnh Ingestion từ {start_date} đến {end_date}. Đang chạy ngầm..."}

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Weather Ingestion Hexagonal (PostgreSQL)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
