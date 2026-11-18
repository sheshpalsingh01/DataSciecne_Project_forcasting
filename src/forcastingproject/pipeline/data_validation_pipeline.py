import os
import sys
from pathlib import Path

# Ensure project root is in sys.path and cwd is project root when run directly
project_root = Path(__file__).resolve().parents[3]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if os.getcwd() != str(project_root):
    os.chdir(project_root)

from src.forcastingproject.config.configuration import ComfigurationManager
from src.forcastingproject.components.data_validation import DataValidation
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.exception.exception import CustomException


STAGE_NAME = "Data Validation"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_validation(self):
        try:
            config = ComfigurationManager()
            data_validation_config = config.get_data_validation_config()

            data_validation = DataValidation(config=data_validation_config)

            # 1) Validate schema columns
            status = data_validation.validation_all_columns()
            logger.info(f"Column validation status: {status}")
            if not status:
                raise ValueError("Ingested data failed column validation.")

            # 2) Load dataframe and handle missing values
            df = data_validation.get_dataframe()
            df_clean = DataValidation.handle_missing_values(df)
            logger.info(f"Missing values filled. Shape: {df_clean.shape}")
            logger.info(f"Null values check after cleaning:\n{df_clean.isnull().sum()}")

        except Exception as e:
            raise CustomException(e, sys)

        


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.initiate_data_validation()
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.error(f">>>>>>>>>>>>>> Stage {STAGE_NAME} failed <<<<<<<<<<<<<<<<")
        raise e
