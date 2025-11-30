from dataclasses import dataclass
from datetime import date
from typing import Optional, Dict, Any

# Dữ liệu chi tiết từng ngày (Cho Line/Scatter/Histogram Daily)
@dataclass
class DailyDataPoint:
    date: date
    weather_code:int
    temp_max: float
    humidity_max: float
    rain_sum: float
    wind_speed_max: float
    radiation_sum: float

# Dữ liệu tổng hợp (Cho Trend/Seasonal/Histogram Weekly-Monthly)
@dataclass
class AggregateDataPoint:
    date: date
    granularity: str
    temp_avg: float
    rain_total: float
    humidity_avg: float

# Dữ liệu Dự báo tổng hợp (Nhiệt độ + Loại thời tiết)
@dataclass
class ForecastSummary:
    forecast_date: date
    predicted_temp: float
    weather_code: int        # Mã gốc (để Frontend hiện icon)

# Dữ liệu Correlation
@dataclass
class CorrelationData:
    matrix: Dict[str, Any]