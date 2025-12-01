import pickle
import os
import numpy as np
from app.interface.modelAI import ModelHandlerPort

class SklearnClassifierAdapter(ModelHandlerPort):
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self) -> None:
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, 'rb') as file:
                    self.model = pickle.load(file)
                print(f">>> [AI Adapter] Classifier loaded from {self.model_path}")
            except Exception as e:
                print(f">>> [AI Adapter Error] {e}")
        else:
            print(f">>> [AI Adapter Warning] Not found: {self.model_path}")

    def predict_class(self, input_vector: list) -> int:
        if not self.model:
            raise Exception("Classifier model is not loaded.")
        
        np_input = np.array(input_vector).reshape(1, -1)
        result = self.model.predict(np_input)
        
        return int(result[0])