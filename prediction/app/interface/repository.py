from typing import Protocol
import pandas as pd
from app.domain.model import PredictionResult

class WeatherRepositoryPort(Protocol):
  def get_latest_days(self, limit: int) -> pd.DataFrame:
    ...
  def save_prediction(self, result: PredictionResult) -> None:
    ...