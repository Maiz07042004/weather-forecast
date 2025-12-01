from typing import Protocol, List
import pandas as pd
from datetime import date
from app.domain.model import AggregateDataPoint, CorrelationData, DailyDataPoint, ForecastSummary

class WeatherRepositoryPort(Protocol):
    def get_daily_series(self, limit: int = 365) -> list[DailyDataPoint]:
        ...

    def get_aggregated_series(self, granularity: str, limit: int = 24) -> list[AggregateDataPoint]:
        ...
    def get_correlation_matrix(self) -> CorrelationData:
        ... 

    def get_latest_forecast(self) -> ForecastSummary:
        ...