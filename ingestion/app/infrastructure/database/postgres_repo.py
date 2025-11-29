from sqlalchemy.orm import Session
from app.interface.repository import WeatherRepositoryPort
from app.domain.model import WeatherDaily
from app.infrastructure.database.orm import WeatherORM

class PostgresRepository(WeatherRepositoryPort):
  def __init__(self, session: Session):
    self.session = session
  def _transform_weather_code(self, code: int) -> int:
    """
    Gom nhóm WMO Weather Code thành 10 nhóm cơ bản để train model hiệu quả hơn.
    """
    # 1. Sky and Cloud (Clear, Cloudy)
    if code in [0, 1, 2, 3]: 
        return 3
    
    # 2. Fog
    if code in [45, 48]: 
        return 45
    
    # 3. Drizzle
    if code in [51, 53, 55]: 
        return 51
    
    # 4. Freezing Drizzle
    if code in [56, 57]: 
        return 56
    
    # 5. Rain
    if code in [61, 63, 65]: 
        return 61
    
    # 6. Freezing Rain
    if code in [66, 67]: 
        return 66
    
    # 7. Snow
    if code in [71, 73, 75, 77]: 
        return 75
    
    # 8. Snow/Rain Showers (Gom nhóm Rain Showers 80-82 vào đây theo yêu cầu)
    if code in [80, 81, 82, 85, 86]: 
        return 80
    
    # 9. Thunderstorm
    if code == 95: 
        return 95
    
    # 10. Thunderstorm with Hail
    if code in [96, 99]: 
        return 96
        
    # Fallback: Giữ nguyên nếu không khớp (hoặc gán về nhóm mặc định tùy ý)
    return code
  def save_bulk(self, data: list[WeatherDaily]) -> None:
    for item in data:
      # Chuyển đổi Weather Code trước khi lưu
      item.weather_code = self._transform_weather_code(item.weather_code)
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