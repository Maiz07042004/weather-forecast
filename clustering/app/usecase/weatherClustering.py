from datetime import timedelta
import pandas as pd
import numpy as np

from app.interface.modelAI import  ModelHandlerPort
from app.interface.repository import WeatherRepositoryPort
from app.domain.model import ClusteringResult

class ClusteringService:
    def __init__(self, repo: WeatherRepositoryPort, model_handler: ModelHandlerPort):
        self.repo = repo
        self.model_handler = model_handler
        
        # Cấu hình Feature (Khớp với 'train_classification_model.py')
        self.FEATURES = [
            'weather_code',       
            'rain_sum',           
            'wind_speed_max',     
            'radiation_sum',     
            'evapotranspiration'       
        ]
        self.WINDOW_SIZE = 7

    def predict_weather_type(self) -> ClusteringResult:
        # 1. Lấy dữ liệu mới nhất
        df = self.repo.get_latest_days(limit=self.WINDOW_SIZE)
        
        if df.empty:
            raise ValueError("No data available for clustering.")

        # 2. Pre-process
        df_features = df[self.FEATURES].fillna(0)
        input_vector = df_features.values.flatten().tolist()

        # 3. Predict Class
        predicted_code = self.model_handler.predict_class(input_vector)

        # 4. Tạo kết quả Domain Object
        last_date = pd.to_datetime(df['date'].iloc[-1]).date()
        forecast_date = last_date + timedelta(days=1)
        
        # Không cần map sang description nữa
        result = ClusteringResult(
            forecast_date=forecast_date,
            predicted_weather_code=predicted_code,
            based_on_last_date=last_date,
            features_used=self.FEATURES
        )

        # 5. Lưu vào Database
        self.repo.save_clustering_result(result)

        return result