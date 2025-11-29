from app.interface.repository import WeatherRepositoryPort

class DashboardService:
    def __init__(self, repo: WeatherRepositoryPort):
        self.repo = repo

    def get_charts_data(self, daily_limit: int = 30):
        return {
            # 1. Dữ liệu Ngày -> Vẽ Line, Scatter, Histogram (Daily)
            "daily_series": self.repo.get_daily_series(limit=daily_limit),
            
            # 2. Dữ liệu Tuần -> Vẽ Trend/Seasonal (Weekly)
            "weekly_series": self.repo.get_aggregated_series(granularity='W', limit=52),
            
            # 3. Dữ liệu Tháng -> Vẽ Trend/Seasonal (Monthly)
            "monthly_series": self.repo.get_aggregated_series(granularity='M', limit=24)
        }

    def get_correlation(self):
        return self.repo.get_correlation_matrix()

    def get_forecast(self):
        return self.repo.get_latest_forecast()