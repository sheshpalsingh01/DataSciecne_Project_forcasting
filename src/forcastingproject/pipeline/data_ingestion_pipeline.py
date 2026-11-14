import os
import sys
from pathlib import Path

# Ensure project root is in sys.path and cwd is project root when run directly
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if os.getcwd() != str(project_root):
    os.chdir(project_root)

from src.forcastingproject.config.configuration import ConfigurationManager, ComfigurationManager
from src.forcastingproject.components.data_ingestion import DataIngestion
from src.forcastingproject.logging.logger import logger

STAGE_NAME = "Data Ingestion"

class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        ingested_data = data_ingestion.initiate_data_ingestion()
        return ingested_data


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.initiate_data_ingestion()
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.error(f">>>>>>>>>>>>>> Stage {STAGE_NAME} failed <<<<<<<<<<<<<<<<")
        raise e
