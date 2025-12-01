from sqlalchemy.orm import Session
import pandas as pd
from app.interface.repository import WeatherRepositoryPort
from app.infrastructure.database.orm import WeatherRawORM, ClusteringORM
from app.domain.model import ClusteringResult

class PostgresClusteringRepository(WeatherRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_latest_days(self, limit: int) -> pd.DataFrame:
        query = self.session.query(WeatherRawORM)\
                    .order_by(WeatherRawORM.date.desc())\
                    .limit(limit)\
                    .statement
        try:
            df = pd.read_sql(query, self.session.bind)
            return df.iloc[::-1]
        except Exception as e:
            print(f"[Repo Error] {e}")
            return pd.DataFrame()

    def save_clustering_result(self, result: ClusteringResult) -> None:
        try:
            orm_obj = ClusteringORM(
                forecast_date=result.forecast_date,
                predicted_code=result.predicted_weather_code,
                based_on_last_date=result.based_on_last_date,
                features_used=result.features_used
            )
            self.session.add(orm_obj)
            self.session.commit()
            print(f">>> [DB] Saved cluster result: Code {result.predicted_weather_code}")
        except Exception as e:
            self.session.rollback()
            print(f"[Repo Error] Save failed: {e}")