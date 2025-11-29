from sqlalchemy import Column, Date, Float, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 1. Bảng Raw Data (Dùng cho Line, Scatter, Histogram theo Ngày)
class WeatherRawORM(Base):
    __tablename__ = "weather_daily"
    date = Column(Date, primary_key=True)
    temp_max = Column(Float)
    temp_min = Column(Float)
    humidity_max = Column(Float)
    rain_sum = Column(Float)
    wind_speed_max = Column(Float)
    radiation_sum = Column(Float)
    evapotranspiration = Column(Float)

# 2. Bảng Aggregate (Dùng cho Trend, Seasonal theo Tuần/Tháng)
class WeatherAggregateORM(Base):
    __tablename__ = "weather_aggregates"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    granularity = Column(String) # 'W' hoặc 'M'
    
    # Các chỉ số trung bình/tổng
    temp_max_avg = Column(Float)
    rain_sum = Column(Float)
    humidity_avg = Column(Float)
    radiation_sum = Column(Float)

# 3. Bảng Prediction (Dự báo nhiệt độ)
class PredictionORM(Base):
    __tablename__ = "weather_predictions"
    id = Column(Integer, primary_key=True)
    forecast_date = Column(Date)
    predicted_temp = Column(Float)
    created_at = Column(DateTime)

# 4. Bảng Clustering (Dự báo loại thời tiết)
class ClusteringORM(Base):
    __tablename__ = "weather_clusters"
    id = Column(Integer, primary_key=True)
    forecast_date = Column(Date)
    predicted_code = Column(Integer)
    created_at = Column(DateTime)

# 5. Bảng Correlation (Ma trận tương quan)
class AnalysisCorrelationORM(Base):
    __tablename__ = "analysis_correlations"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    matrix = Column(JSON)