from functools import wraps
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.score.handler import RequestHandler, get_handler
from app.log import get_logger
from app import params as params
from app.errors import InvalidModelVersion, InvalidInput

from app.score.schema import ScoreModel

SCORE_PREFIX = "/v1/score"

router = APIRouter(prefix=SCORE_PREFIX, tags=["score"])

def common_exception_handler(func):
    @wraps(func)
    async def inner_function(*args, **kwargs):
        logger = get_logger(__name__)
        try:
            result = await func(*args, **kwargs)
        except InvalidModelVersion as e:
            logger.exception(e)
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Model version does not exist. {e}") from e
        except InvalidInput as e:
            logger.exception(e)
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"{e}") from e
        return result
    return inner_function


@router.post("/stream",response_model=List[ScoreModel], response_model_exclude_none=True)
@common_exception_handler
async def stream_score(
    model_version: str = params.model_version,
    input: Dict = params.input,
    handler: RequestHandler = Depends(get_handler)
):
    if len(input) != 1:
        raise InvalidInput("Use v1/score/batch endpoint for batch processing.")
    inference = handler.score(input=input, version=model_version)
    return inference

@router.post("/batch",response_model=List[ScoreModel], response_model_exclude_none=True)
@common_exception_handler
async def batch_score(
    model_version: str = params.model_version,
    input: Dict = params.input,
    handler: RequestHandler = Depends(get_handler)
):
    inference = handler.score(input=input, version=model_version)
    return inference
