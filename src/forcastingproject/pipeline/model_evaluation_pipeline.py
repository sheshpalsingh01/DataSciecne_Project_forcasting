import argparse
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[3]
    sys.path.insert(0, str(project_root))
    os.chdir(project_root)

from src.forcastingproject.components.model_evaluation import ModelEvaluation
from src.forcastingproject.config.configuration import ConfigurationManager
from src.forcastingproject.logging.logger import logger


STAGE_NAME = "Model Evaluation"


class ModelEvaluationTrainingPipeline:
    def initiate_model_evaluation(self, *, local_only: bool = False) -> dict[str, float]:
        config = ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        return model_evaluation.initiate_model_evaluation(local_only=local_only)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate the trained sales model.")
    parser.add_argument("--local-only", action="store_true", help="Save metrics to JSON only.")
    args = parser.parse_args()

    try:
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} started <<<<<<<<<<<<<<<<")
        ModelEvaluationTrainingPipeline().initiate_model_evaluation(local_only=args.local_only)
        logger.info(f">>>>>>>>>>>>>> Stage {STAGE_NAME} completed <<<<<<<<<<<<<<<<")
    except Exception:
        logger.exception(f">>>>>>>>>>>>>> Stage {STAGE_NAME} failed <<<<<<<<<<<<<<<<")
        raise
