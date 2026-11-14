from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    train_data: Path
    store_data: Path

@dataclass(frozen=True)
class DataValidationConfig:
    root_dir : Path
    data_file_dir: Path
    status_file: Path