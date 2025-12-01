from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class PredictionResult:
  forecast_date: date
  predicted_temp: float
  based_on_last_date: date
  features_used: List[str]