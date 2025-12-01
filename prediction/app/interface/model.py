from typing import Protocol, List

class ModelHandlerPort(Protocol):
  def load_model(self) -> None:
    ...
  
  def predict(self, input_vector: List[float]) -> float:
    ...