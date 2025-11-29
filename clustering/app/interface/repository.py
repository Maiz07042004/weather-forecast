from typing import Protocol, List
import pandas as pd
from datetime import date
from app.domain.model import ClusteringResult

# Port 1: Giao tiếp Database
class WeatherRepositoryPort(Protocol):
    def get_latest_days(self, limit: int) -> pd.DataFrame:
        """Lấy N ngày dữ liệu mới nhất"""
        ...

    def save_clustering_result(self, result: ClusteringResult) -> None:
        """Lưu kết quả phân loại vào DB"""
        ...