from datetime import timedelta
import pandas as pd
import numpy as np

from app.interface.repository import WeatherRepositoryPort
from app.interface.model import ModelHandlerPort
from app.domain.model import PredictionResult

class PredictionService:
    def __init__(self, repo: WeatherRepositoryPort, model_handler: ModelHandlerPort):
        self.repo = repo
        self.model_handler = model_handler
        
        self.FEATURES = [
            'temp_max', 'temp_min', 'humidity_max', 
            'radiation_sum', 'evapotranspiration'
        ]
        self.WINDOW_SIZE = 7

    def predict_next_day(self) -> PredictionResult:
        df = self.repo.get_latest_days(limit=self.WINDOW_SIZE)
        
        if len(df) < self.WINDOW_SIZE:
            raise ValueError(f"Not enough data. Need {self.WINDOW_SIZE} days, got {len(df)}")

        # Pre-process
        df_features = df[self.FEATURES].fillna(0)
        
        # Scikit-learn cần input dạng numpy array 2D
        input_vector = df_features.values.flatten().tolist()

        # Predict
        predicted_val = self.model_handler.predict(input_vector)

        # Tạo kết quả Domain Object
        last_date = pd.to_datetime(df['date'].iloc[-1]).date()
        forecast_date = last_date + timedelta(days=1)

        result = PredictionResult(
            forecast_date=forecast_date,
            predicted_temp=round(predicted_val, 2),
            based_on_last_date=last_date,
            features_used=self.FEATURES
        )

        # Lưu vào Database
        self.repo.save_prediction(result)

        return result