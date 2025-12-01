from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import json

from app.interface.repository import AnalysisRepositoryPort
from app.domain.model import WeatherAggregate, CorrelationMatrix
from app.infrastructure.database.orm import WeatherRawORM, WeatherAggregateORM, CorrelationORM

class PostgresAnalysisRepository(AnalysisRepositoryPort):
    def __init__(self, session: Session):
        self.session = session

    def get_raw_data(self) -> pd.DataFrame:
        query = self.session.query(WeatherRawORM)
        try:
            pd.read_sql(query.statement, self.session.bind).to_csv("debug_raw_data.csv")
            # Dùng pandas đọc trực tiếp từ SQL connection
            return pd.read_sql(query.statement, self.session.bind)         
        except Exception as e:
            print(f"[Repo Error] Reading raw data: {e}")
            return pd.DataFrame()

    def save_aggregates(self, data: List[WeatherAggregate]) -> None:
        try:
            count_update = 0
            count_insert = 0
            
            for item in data:
                existing = self.session.query(WeatherAggregateORM).filter_by(
                    date=item.date, 
                    granularity=item.granularity
                ).first()

                if existing:                    
                    existing.temp_max_avg = item.temp_max_avg
                    existing.temp_min_avg = item.temp_min_avg
                    existing.rain_sum = item.rain_sum
                    existing.humidity_avg = item.humidity_avg
                    existing.wind_speed_max = item.wind_speed_max
                    existing.radiation_sum = item.radiation_sum
                    count_update += 1
                else:
                    new_obj = WeatherAggregateORM(
                        date=item.date,
                        granularity=item.granularity,
                        temp_max_avg=item.temp_max_avg,
                        temp_min_avg=item.temp_min_avg,
                        rain_sum=item.rain_sum,
                        humidity_avg=item.humidity_avg,
                        wind_speed_max=item.wind_speed_max,
                        radiation_sum=item.radiation_sum
                    )
                    self.session.add(new_obj)
                    count_insert += 1
            self.session.commit()
            print(f"--- [DB] Saved {count_insert} new aggregates, updated {count_update} existing aggregates ---")
        except Exception as e:
            self.session.rollback()
            print(f"[Repo Error] Saving aggregates: {e}")

    def save_correlation(self, data: CorrelationMatrix) -> None:
        try:
            clean_matrix = json.loads(json.dumps(data.matrix).replace('NaN', 'null'))
            orm_obj = CorrelationORM(matrix=clean_matrix)
            self.session.add(orm_obj)
            self.session.commit()
            print("--- [DB] Saved correlation matrix ---")
        except Exception as e:
            self.session.rollback()
            print(f"[Repo Error] Saving correlation: {e}")