from sqlalchemy import Column, Date, Float, Integer, String, JSON, UniqueConstraint, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

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

class WeatherAggregateORM(Base):
  __tablename__ = "weather_aggregates"

  id = Column(Integer, primary_key=True, index=True)
  date = Column(Date, index=True)
  granularity = Column(String)
  
  temp_max_avg = Column(Float)
  temp_min_avg = Column(Float)
  rain_sum = Column(Float)
  humidity_avg = Column(Float)
  wind_speed_max = Column(Float)
  radiation_sum = Column(Float)

  __table_args__ = (UniqueConstraint('date', 'granularity', name='uq_date_gran_analysis'),)

class CorrelationORM(Base):
  __tablename__ = "analysis_correlations"

  id = Column(Integer, primary_key=True)
  created_at = Column(DateTime, default=datetime.now)
  matrix = Column(JSON)