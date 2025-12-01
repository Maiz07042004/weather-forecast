from typing import Protocol
import pandas as pd
from app.domain.model import ClusteringResult

class WeatherRepositoryPort(Protocol):
    def get_latest_days(self, limit: int) -> pd.DataFrame:
        ...

    def save_clustering_result(self, result: ClusteringResult) -> None:
        ...