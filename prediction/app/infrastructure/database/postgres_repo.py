from sqlalchemy.orm import Session
import pandas as pd
from app.interface.repository import WeatherRepositoryPort
from app.infrastructure.database.orm import WeatherRawORM, PredictionORM
from app.domain.model import PredictionResult

class PostgresPredictionRepository(WeatherRepositoryPort):
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

    def save_prediction(self, result: PredictionResult) -> None:
        try:
            orm_obj = PredictionORM(
                forecast_date=result.forecast_date,
                predicted_temp=result.predicted_temp,
                based_on_last_date=result.based_on_last_date,
                features_used=result.features_used
            )
            self.session.add(orm_obj)
            self.session.commit()
            print(f">>> [DB] Saved prediction for date: {result.forecast_date}")
        except Exception as e:
            self.session.rollback()
            print(f"[Repo Error] Saving prediction failed: {e}")