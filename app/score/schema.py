from typing import Dict, List, Optional, Any
from app.model import CamelModel

class ScoreModel(CamelModel):
    patient: str
    input: Optional[float]
    progression: float
    model_version: Optional[str]
