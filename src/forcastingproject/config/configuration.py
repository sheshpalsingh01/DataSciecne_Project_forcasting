from pathlib import Path
from src.forcastingproject.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.forcastingproject.utils.common import read_yaml_file, create_directories
from src.forcastingproject.entity import DataIngestionConfig, DataValidationConfig

class ConfigurationManager:
    def __init__(
        self,
        config_file_path: Path = CONFIG_FILE_PATH,
        params_file_path: Path = PARAMS_FILE_PATH,
        schema_file_path: Path = SCHEMA_FILE_PATH
    ):
        self.config = read_yaml_file(config_file_path)
        self.params = read_yaml_file(params_file_path)
        self.schema = read_yaml_file(schema_file_path)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            train_data=Path(config.train_data),
            store_data=Path(config.store_data)
        )
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        schema = self.schema.COLUMNS

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            status_file=Path(config.status_file),
            data_file_dir=Path(config.data_file_dir),
            all_schema=schema
        )
        return data_validation_config

# Alias for backward compatibility
ComfigurationManager = ConfigurationManager

