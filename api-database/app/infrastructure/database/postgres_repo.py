from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.infrastructure.database.orm import (
    WeatherRawORM, WeatherAggregateORM, 
    PredictionORM, ClusteringORM, AnalysisCorrelationORM
)
from app.domain.model import (
    DailyDataPoint, AggregateDataPoint, 
    ForecastSummary, CorrelationData
)
from app.interface.repository import WeatherRepositoryPort

class WeatherRepository(WeatherRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_daily_series(self, limit: int = 365) -> list[DailyDataPoint]:
        """Lấy dữ liệu thô theo ngày (cho Line Chart, Scatter Daily)"""
        query = self.session.query(WeatherRawORM)\
                    .order_by(desc(WeatherRawORM.date))\
                    .limit(limit)
        
        results = []
        for row in query.all():
            results.append(DailyDataPoint(
                date=row.date,
                temp_max=row.temp_max,
                humidity_max=row.humidity_max,
                rain_sum=row.rain_sum,
                wind_speed_max=row.wind_speed_max,
                radiation_sum=row.radiation_sum
            ))
        return results[::-1] # Đảo ngược: Quá khứ -> Hiện tại

    def get_aggregated_series(self, granularity: str, limit: int = 24) -> list[AggregateDataPoint]:
        """Lấy dữ liệu tổng hợp (cho Trend, Seasonal)"""
        query = self.session.query(WeatherAggregateORM)\
                    .filter(WeatherAggregateORM.granularity == granularity)\
                    .order_by(desc(WeatherAggregateORM.date))\
                    .limit(limit)
        
        results = []
        for row in query.all():
            results.append(AggregateDataPoint(
                date=row.date,
                granularity=row.granularity,
                temp_avg=row.temp_max_avg,
                rain_total=row.rain_sum,
                humidity_avg=row.humidity_avg
            ))
        return results[::-1]

    def get_correlation_matrix(self) -> CorrelationData:
        """Lấy ma trận tương quan mới nhất"""
        record = self.session.query(AnalysisCorrelationORM)\
                     .order_by(desc(AnalysisCorrelationORM.id))\
                     .first()
        if record:
            return CorrelationData(matrix=record.matrix)
        return CorrelationData(matrix={})

    def get_latest_forecast(self) -> ForecastSummary:
        """Kết hợp dự báo Nhiệt độ và Phân loại thời tiết"""
        pred = self.session.query(PredictionORM).order_by(desc(PredictionORM.id)).first()
        cluster = self.session.query(ClusteringORM).order_by(desc(ClusteringORM.id)).first()
        
        if not pred:
            return None

        # Logic map mã code sang text hiển thị
        w_code = cluster.predicted_code if cluster else -1
        w_desc = "Không rõ"
        
        # Mapping đơn giản (Bạn có thể mở rộng)
        if w_code == 1: w_desc = "Nắng đẹp/Có mây"
        elif w_code == 2: w_desc = "Sương mù"
        elif w_code == 3: w_desc = "Mưa phùn"
        elif w_code == 5: w_desc = "Mưa"
        elif w_code >= 9: w_desc = "Giông bão"
        
        return ForecastSummary(
            forecast_date=pred.forecast_date,
            predicted_temp=pred.predicted_temp,
            weather_type=w_desc,
            weather_code=w_code
        )