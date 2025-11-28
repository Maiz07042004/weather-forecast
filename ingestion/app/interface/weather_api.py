from typing import List, Protocol
from app.domain.model import WeatherDaily

class WeatherApiClientPort(Protocol):
  def fetch_daily_data(self, start_date: str, end_date: str) -> List[WeatherDaily]:
    ...