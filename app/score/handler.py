from dataclasses import dataclass
import pickle
from typing import Dict, List, Optional

import numpy as np

from app import params
from app.errors import InvalidInput, InvalidModelVersion
from app.log import get_logger
from app.score.schema import ScoreModel


@dataclass(frozen=True)
class RequestHandler:
    include_version: bool
    include_input: bool
    logger = get_logger(__name__)

    def score(self, version: str, input_data: Dict) -> List[ScoreModel]:
        self.logger.info(f"Scoring for {input_data}")
        key = input_data.keys()
        features = list(input_data.values())
        if not all(isinstance(x, list) for x in features):
            raise InvalidInput("All inputs must be of datatype List[float].")
        if not all(isinstance(x[0], float) for x in features):
            raise InvalidInput("All inputs must be of datatype List[float].")
        filename = f"app/model/db_score_{version}.sav"
        try:
            with open(filename, "rb") as file:
                loaded_model = pickle.load(file)
        except FileNotFoundError as e:
            raise InvalidModelVersion(version)
        inference = loaded_model.predict(features)
        return self._marshall_score(keys=key, scores=inference, model_version=version, input_data=features)

    def _marshall_score(
        self, keys: List, scores: np.array, model_version: Optional[str] = None, input_data: Optional[List] = None
    ) -> List[ScoreModel]:
        input_data = [list(i)[0] for i in input_data]
        inference = [list(i)[0] for i in scores]
        result = list(zip(keys, input_data, inference))
        return [
            ScoreModel(
                patient=key,
                progression=score,
                model_version=model_version if self.include_version else None,
                input_data=feature if self.include_input else None,
            )
            for key, feature, score in result
        ]


async def get_handler(
    include_version: bool = params.include_model_version, include_input: bool = params.include_input
) -> RequestHandler:
    return RequestHandler(include_version, include_input)
