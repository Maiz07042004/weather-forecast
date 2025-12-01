import pickle
import os
import numpy as np
from app.interface.model import ModelHandlerPort

class SklearnModelAdapter(ModelHandlerPort):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self) -> None:
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as file:
                    self.model = pickle.load(file)
                print(f">>> [AI Adapter] Model loaded from {self.model_path}")
            except Exception as e:
                print(f">>> [AI Adapter Error] {e}")
        else:
            print(f">>> [AI Adapter Warning] File not found: {self.model_path}")

    def predict(self, input_vector: list) -> float:
        if not self.model:
            raise Exception("Model is not loaded.")
        
        np_input = np.array(input_vector).reshape(1, -1)
        result = self.model.predict(np_input)
        return float(result[0])