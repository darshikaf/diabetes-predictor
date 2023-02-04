from dataclasses import dataclass
from typing import Dict

from app import params
from app.errors import InvalidInput
from app.log import get_logger
from app.train.schema import TrainInfo
from app.train.simple_linear_regr import SimpleLinearRegression
from app.train.simple_linear_regr_utils import evaluate, generate_data, save_model


@dataclass(frozen=True)
class RequestHandler:
    include_version: bool
    include_inputs: bool
    logger = get_logger(__name__)

    def train(self, model_version: str, training_data: Dict, use_internal_data: bool) -> TrainInfo:
        self._validate_training_data_schema(training_data=training_data, use_internal_data=use_internal_data)
        lr = training_data["lr"]
        iterations = training_data["epochs"]
        if use_internal_data:
            self.logger.info("Generating data...")
            X_train, y_train, X_test, y_test = generate_data()
            model = SimpleLinearRegression(iterations=iterations, lr=lr)
            self.logger.info("Model training...")
            model.fit(X_train, y_train)
            predicted = model.predict(X_test)
            r2_value = evaluate(model, X_test, y_test, predicted)
            filepath = save_model(model=model, model_version=model_version)
        else:
            raise NotImplementedError
        return TrainInfo(r2=r2_value, model_location=filepath)

    def _validate_training_data_schema(self, training_data: Dict, use_internal_data: bool):
        if use_internal_data:
            print(list(training_data.keys()))
            if list(training_data.keys()) != ["lr", "epochs"]:
                raise InvalidInput("Incomplete data provided for retraining.")
        else:
            if not ["features", "target", "learning_rate", "epochs"] not in training_data:
                raise InvalidInput("Incomplete data provided for retraining.")


async def get_handler(
    include_version: bool = params.include_model_version, include_input: bool = params.include_input
) -> RequestHandler:
    return RequestHandler(include_version, include_input)
