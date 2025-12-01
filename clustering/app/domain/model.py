from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class ClusteringResult:
    forecast_date: date
    predicted_weather_code: int
    based_on_last_date: date
    features_used: List[str]