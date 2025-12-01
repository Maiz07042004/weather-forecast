# app/adapters/database/orm.py (hoặc models.py cũ)
from sqlalchemy import Column, Date, Float, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WeatherORM(Base):
  __tablename__ = "weather_daily"

  date = Column(Date, primary_key=True, index=True)
  weather_code = Column(Integer)
  temp_max = Column(Float)
  temp_min = Column(Float)
  humidity_max = Column(Float) 
  humidity_min = Column(Float)
  rain_sum = Column(Float)
  wind_speed_max = Column(Float)
  wind_direction = Column(Float)
  radiation_sum = Column(Float)       # MJ/m²
  evapotranspiration = Column(Float)  # mm