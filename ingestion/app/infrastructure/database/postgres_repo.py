from sqlalchemy.orm import Session
from app.interface.repository import WeatherRepositoryPort
from app.domain.model import WeatherDaily
from app.infrastructure.database.orm import WeatherORM

class PostgresRepository(WeatherRepositoryPort):
  def __init__(self, session: Session):
    self.session = session

  def save_bulk(self, data: list[WeatherDaily]) -> None:
    for item in data:
      # Mapper: Domain Entity -> DB ORM
      record = WeatherORM(
          date=item.date,
          weather_code=item.weather_code,
          temp_max=item.temp_max,
          temp_min=item.temp_min,
          humidity_max=item.humidity_max,
          humidity_min=item.humidity_min,
          rain_sum=item.rain_sum,
          wind_speed_max=item.wind_speed_max,
          wind_direction=item.wind_direction,
          radiation_sum=item.radiation_sum,
          evapotranspiration=item.evapotranspiration
      )
      # Upsert (Merge): Nếu trùng ngày thì update, chưa có thì insert
      self.session.merge(record)
    
    self.session.commit()