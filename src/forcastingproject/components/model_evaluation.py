import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.forcastingproject.entity import ModelEvaluationConfig
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.utils.common import save_json


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def initiate_model_evaluation(self, *, local_only: bool = False) -> dict[str, float]:
        test_data = pd.read_csv(self.config.test_data_path)
        features = test_data.drop(columns=self.config.target_column)
        target = test_data[self.config.target_column]
        model = joblib.load(self.config.model_path)
        predictions = model.predict(features)

        metrics = {
            "rmse": float(mean_squared_error(target, predictions) ** 0.5),
            "mae": float(mean_absolute_error(target, predictions)),
            "r2": float(r2_score(target, predictions)),
        }
        save_json(self.config.metrics_path, metrics)
        logger.info(f"Saved evaluation metrics to {self.config.metrics_path}")

        if not local_only:
            self.log_to_mlflow(model, features.head(), predictions[:5], metrics)

        return metrics

    def log_to_mlflow(self, model, input_example, predictions, metrics):
        import mlflow
        import mlflow.sklearn
        from mlflow.models import infer_signature

        mlflow.set_tracking_uri(self.config.tracking_uri)
        mlflow.set_experiment(self.config.experiment_name)

        with mlflow.start_run(run_name="random-forest-evaluation") as run:
            mlflow.log_params(self.config.model_params)
            mlflow.log_metrics(metrics)
            mlflow.log_artifact(str(self.config.metrics_path))
            mlflow.sklearn.log_model(
                sk_model=model,
                name="model",
                input_example=input_example,
                signature=infer_signature(input_example, predictions),
                registered_model_name=self.config.registered_model_name,
            )
            logger.info(f"Logged evaluation to MLflow run {run.info.run_id}")
