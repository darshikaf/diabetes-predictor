from typing import Dict

from fastapi import APIRouter, Depends

from app import params
from app.train.handler import RequestHandler, get_handler
from app.train.schema import TrainInfo

TRAIN_PREFIX = "/v1/train"

router = APIRouter(prefix=TRAIN_PREFIX, tags=["train"])


@router.post("/retrain", response_model=TrainInfo, response_model_exclude_none=True)
async def train(
    model_version: str = params.model_version,
    training_data: Dict = params.training_data,
    use_internal_data: bool = params.use_internal_data,
    handler: RequestHandler = Depends(get_handler),
):
    return handler.train(model_version=model_version, training_data=training_data, use_internal_data=use_internal_data)
