# app/adapters/database/orm.py (hoặc models.py cũ)
from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WeatherORM(Base):
  __tablename__ = "weather_daily"

  date = Column(Date, primary_key=True, index=True)
  weather_code = Column(Integer)
  
  # Nhiệt độ
  temp_max = Column(Float)
  temp_min = Column(Float)
  
  # Độ ẩm (MỚI)
  humidity_max = Column(Float) 
  humidity_min = Column(Float)
  
  # Mưa & Gió
  rain_sum = Column(Float)
  wind_speed_max = Column(Float)
  wind_direction = Column(Float) # Hướng gió chủ đạo (độ)
  
  # Năng lượng & Bốc hơi
  radiation_sum = Column(Float)       # MJ/m²
  evapotranspiration = Column(Float)  # mm