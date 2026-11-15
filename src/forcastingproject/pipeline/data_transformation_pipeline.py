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
from src.forcastingproject.components.data_transformation import DataTransformation
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.exception.exception import CustomException
import traceback, datetime

STAGE_NAME ="Data Transformation"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            config = ComfigurationManager()
            transform_config = config.get_data_transformation_config()
            transformer = DataTransformation(config=transform_config)
            transformer.explor_data_analysis()
            transformer.initiate_data_transformation()
        except Exception as e:
            err_path = Path("artifacts/reports") / f"error_{datetime.datetime.now():%Y%m%d_%H%M%S}.log"
            err_path.parent.mkdir(parents=True, exist_ok=True)
            err_path.write_text(traceback.format_exc())
            print(f"Error report written to: {err_path}")
            raise e
        


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.initiate_data_transformation()
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<")
    except Exception as e:
        logger.error(f">>>>>>>>>>>>>> Stage {STAGE_NAME} failed <<<<<<<<<<<<<<<<")
        raise e
