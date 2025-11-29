from sqlalchemy import Column, Date, Float, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# Bảng Raw (Chỉ đọc)
class WeatherRawORM(Base):
    __tablename__ = "weather_daily"
    date = Column(Date, primary_key=True)
    weather_code = Column(Integer)
    temp_max = Column(Float)
    temp_min = Column(Float)
    humidity_max = Column(Float)
    rain_sum = Column(Float)
    wind_speed_max = Column(Float)
    radiation_sum = Column(Float)
    evapotranspiration = Column(Float)


class ClusteringORM(Base):
    __tablename__ = "weather_clusters"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    forecast_date = Column(Date)
    predicted_code = Column(Integer)
    # description = Column(String)  <-- Đã xóa
    based_on_last_date = Column(Date)
    features_used = Column(JSON)