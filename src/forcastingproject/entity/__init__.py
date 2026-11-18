from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    train_data: Path
    store_data: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_file_dir: Path
    status_file: Path
    all_schema: dict

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    reports_dir: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    model_name: str
    target_column: str
    n_estimators: int
    max_depth: int | None
    random_state: int
    n_jobs: int


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metrics_path: Path
    target_column: str
    tracking_uri: str
    experiment_name: str
    model_params: dict
    registered_model_name: str
