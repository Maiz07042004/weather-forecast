import requests
from datetime import datetime
from typing import List
from app.interface.weather_api import WeatherApiClientPort
from app.domain.model import WeatherDaily

class OpenMeteoClient(WeatherApiClientPort):
  def __init__(self, lat: float, lon: float):
    self.lat = lat
    self.lon = lon
    self.base_url = "https://archive-api.open-meteo.com/v1/archive"

  def fetch_daily_data(self, start_date: str, end_date: str) -> List[WeatherDaily]:
    params = {
      "latitude": self.lat,
      "longitude": self.lon,
      "start_date": start_date,
      "end_date": end_date,
      "daily": "weather_code,temperature_2m_max,temperature_2m_min,relative_humidity_2m_max,relative_humidity_2m_min,apparent_temperature_max,apparent_temperature_min,sunrise,sunset,daylight_duration,sunshine_duration,precipitation_sum,rain_sum,snowfall_sum,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration",
      "timezone": "auto"
    }
    
    resp = requests.get(self.base_url, params=params)
    resp.raise_for_status()
    json_data = resp.json().get("daily", {})
    
    if not json_data: return []

    # Chuyển cột thành dòng
    results = []
    dates = json_data["time"]
    for i in range(len(dates)):
      entity = WeatherDaily(
        date=datetime.strptime(dates[i], "%Y-%m-%d").date(),
        weather_code=json_data["weather_code"][i],
        temp_max=json_data["temperature_2m_max"][i],
        temp_min=json_data["temperature_2m_min"][i],
        humidity_max=json_data["relative_humidity_2m_max"][i],
        humidity_min=json_data["relative_humidity_2m_min"][i],
        rain_sum=json_data["rain_sum"][i],
        wind_speed_max=json_data["wind_speed_10m_max"][i],
        wind_direction=json_data["wind_direction_10m_dominant"][i],
        radiation_sum=json_data["shortwave_radiation_sum"][i],
        evapotranspiration=json_data["et0_fao_evapotranspiration"][i]
      )
      results.append(entity)       
    return results