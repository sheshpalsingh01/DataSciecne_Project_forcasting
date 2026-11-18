import os
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(project_root))
    os.chdir(project_root)

from src.forcastingproject.components.model_trainer import ModelTrainer
from src.forcastingproject.config.configuration import ConfigurationManager
from src.forcastingproject.logging.logger import logger


STAGE_NAME = "Model Trainer"


class ModelTrainerTrainingPipeline:
    def initiate_model_trainer(self) -> Path:
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config=model_trainer_config)
        return model_trainer.initiate_model_trainer()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<<<<<")
        ModelTrainerTrainingPipeline().initiate_model_trainer()
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<")
    except Exception:
        logger.exception(f">>>>>>>>>>>>>> Stage {STAGE_NAME} failed <<<<<<<<<<<<<<<<")
        raise
