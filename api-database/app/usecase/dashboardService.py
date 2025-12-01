from app.interface.repository import WeatherRepositoryPort

class DashboardService:
    def __init__(self, repo: WeatherRepositoryPort):
        self.repo = repo

    def get_charts_data(self, daily_limit: int = 360):
        return {
            "daily_series": self.repo.get_daily_series(limit=daily_limit),            
            "weekly_series": self.repo.get_aggregated_series(granularity='W', limit=52),            
            "monthly_series": self.repo.get_aggregated_series(granularity='ME', limit=24)
        }

    def get_correlation(self):
        return self.repo.get_correlation_matrix()

    def get_forecast(self):
        return self.repo.get_latest_forecast()