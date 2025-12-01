from dataclasses import dataclass
from datetime import date
from typing import Dict, Any

@dataclass
class WeatherAggregate:
    date: date
    granularity: str  # 'W' hoặc 'ME'
    temp_max_avg: float
    temp_min_avg: float
    rain_sum: float
    humidity_avg: float
    wind_speed_max: float
    radiation_sum: float

@dataclass
class CorrelationMatrix:
    matrix: Dict[str, Any]