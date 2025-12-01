from typing import Protocol, List, Dict
import pandas as pd
from app.domain.model import WeatherAggregate, CorrelationMatrix

class AnalysisRepositoryPort(Protocol):
  def get_raw_data(self) -> pd.DataFrame:
    ...

  def save_aggregates(self, data: List[WeatherAggregate]) -> None:
    ...

  def save_correlation(self, data: CorrelationMatrix) -> None:
    ...