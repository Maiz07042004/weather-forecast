from dataclasses import dataclass
from datetime import date

@dataclass
class WeatherDaily:
  date: date
  weather_code: int

  # Nhiệt độ
  temp_max: float
  temp_min: float

  # Độ ẩm (MỚI)
  humidity_max: float
  humidity_min: float

  # Mưa & Gió
  rain_sum: float
  wind_speed_max: float
  wind_direction: float # Hướng gió

  # Năng lượng & Khác
  radiation_sum: float       # Bức xạ mặt trời
  evapotranspiration: float  # Độ bốc hơi