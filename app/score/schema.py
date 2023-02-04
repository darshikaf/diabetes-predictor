from typing import Optional

from app.model import CamelModel


class ScoreModel(CamelModel):
    patient: str
    input_data: Optional[float]
    progression: float
    model_version: Optional[str]
