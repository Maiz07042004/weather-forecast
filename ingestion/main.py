from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import os
from dotenv import load_dotenv

from app.infrastructure.database.orm import Base
from app.infrastructure.database.postgres_repo import PostgresRepository
from app.infrastructure.openmeteo.client import OpenMeteoClient
from app.usecase.ingestion import WeatherIngestionService

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
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_ingestion_service(db_session):
    repo = PostgresRepository(session=db_session)
    client = OpenMeteoClient(lat=LAT, lon=LON)
    service = WeatherIngestionService(api_client=client, repo=repo)
    return service

def job_ingestion_5min():
    print("--- [CRON] Bắt đầu Job Ingestion định kỳ ---")
    db = SessionLocal()
    try:
        service = get_ingestion_service(db)
        
        end_d = date.today()
        start_d = end_d - timedelta(days=7)
        
        service.execute(
            start_date=start_d.strftime("%Y-%m-%d"),
            end_date=end_d.strftime("%Y-%m-%d")
        )
    except Exception as e:
        print(f"--- [CRON ERROR] {e}")
    finally:
        db.close()
    print("--- [CRON] Kết thúc Job Ingestion định kỳ ---")


# Cấu hình FastAPI & Scheduler Lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):

    print(">>> Khởi động Scheduler...")
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(job_ingestion_5min, 'interval', minutes=5)
    scheduler.start()

    db = SessionLocal()
    try:
        service = get_ingestion_service(db)
        
        end_d = date.today()
        start_d = end_d - timedelta(days=1100)
        
        service.execute(
            start_date=start_d.strftime("%Y-%m-%d"),
            end_date=end_d.strftime("%Y-%m-%d")
        )
    except Exception as e:
        print(f"--- [CRON ERROR] {e}")
    finally:
        db.close()
    
    yield
    
    print(">>> Dừng Scheduler...")
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.post("/ingest/manual")
def manual_ingest(start_date: str, end_date: str, background_tasks: BackgroundTasks):
    def task():
        db = SessionLocal()
        try:
            service = get_ingestion_service(db)
            service.execute(start_date, end_date)
        finally:
            db.close()

    background_tasks.add_task(task)
    return {"message": f"Đã nhận lệnh Ingestion từ {start_date} đến {end_date}. Đang chạy ngầm..."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
