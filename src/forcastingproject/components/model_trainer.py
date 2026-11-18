from pathlib import Path
from tempfile import TemporaryDirectory

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.forcastingproject.entity import ModelTrainerConfig
from src.forcastingproject.logging.logger import logger


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def initiate_model_trainer(self) -> Path:
        config = self.config
        try:
            training_data = pd.read_csv(config.train_data_path)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Training data missing at {config.train_data_path}. Run Stage 03 first."
            ) from exc

        if config.target_column not in training_data.columns:
            raise ValueError(
                f"Target column {config.target_column!r} missing from {config.train_data_path}"
            )

        features = training_data.drop(columns=config.target_column)
        target = training_data[config.target_column]
        model = RandomForestRegressor(
            n_estimators=config.n_estimators,
            max_depth=config.max_depth,
            random_state=config.random_state,
            n_jobs=config.n_jobs,
        )
        logger.info(
            f"Training RandomForestRegressor on {features.shape[0]:,} rows "
            f"and {features.shape[1]} features from {config.train_data_path}"
        )
        model.fit(features, target)

        model_path = config.root_dir / config.model_name
        with TemporaryDirectory(dir=config.root_dir) as temp_dir:
            temp_path = Path(temp_dir) / config.model_name
            joblib.dump(model, temp_path)
            temp_path.replace(model_path)

        logger.info(f"Saved trained model to {model_path}")
        return model_path
