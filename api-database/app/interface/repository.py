from typing import Protocol, List
import pandas as pd
from datetime import date
from app.domain.model import AggregateDataPoint, CorrelationData, DailyDataPoint, ForecastSummary

# Port 1: Giao tiếp Database
class WeatherRepositoryPort(Protocol):
    def get_daily_series(self, limit: int = 365) -> list[DailyDataPoint]:
        """Lấy N ngày dữ liệu mới nhất"""
        ...

    def get_aggregated_series(self, granularity: str, limit: int = 24) -> list[AggregateDataPoint]:
        """Lấy dữ liệu tổng hợp theo độ chi tiết (Tuần/Tháng)"""
        ...
    def get_correlation_matrix(self) -> CorrelationData:
        ... 

    def get_latest_forecast(self) -> ForecastSummary:
        """Lấy dự báo mới nhất"""
        ...