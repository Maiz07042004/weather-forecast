from typing import Protocol
from app.domain.model import WeatherDaily

class WeatherRepositoryPort(Protocol):
  def save_bulk(self, data: list[WeatherDaily]) -> None:
    ...