from dataclasses import dataclass
from datetime import date

@dataclass
class WeatherDaily:
  date: date
  weather_code: int

  temp_max: float
  temp_min: float

  humidity_max: float
  humidity_min: float

  rain_sum: float
  wind_speed_max: float
  wind_direction: float

  radiation_sum: float       # Bức xạ mặt trời
  evapotranspiration: float  # Độ bốc hơi