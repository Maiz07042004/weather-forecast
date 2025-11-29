from typing import Protocol, List
class ModelHandlerPort(Protocol):
    def load_model(self) -> None:
        """Load model từ file"""
        ...
    
    def predict_class(self, input_vector: list) -> int:
        """Dự đoán Nhãn (Class) từ vector đầu vào"""
        ...