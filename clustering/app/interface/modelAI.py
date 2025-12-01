from typing import Protocol, List
class ModelHandlerPort(Protocol):
    def load_model(self) -> None:
        ...
    
    def predict_class(self, input_vector: list) -> int:
        ...