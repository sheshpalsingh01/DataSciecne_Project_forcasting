from src.forcastingproject.pipeline.data_ingestion_pipeline import DataIngestionTrainingPipeline
from src.forcastingproject.pipeline.data_validation_pipeline import DataValidationTrainingPipeline
from src.forcastingproject.pipeline.data_transformation_pipeline import DataTransformationTrainingPipeline
from src.forcastingproject.pipeline.model_trainer_pipeline import ModelTrainerTrainingPipeline
from src.forcastingproject.logging.logger import logger

STAGE_NAME1 = "Data Ingestion Stage"
STAGE_NAME2 = "Data Validation Stage"
STAGE_NAME3 = "Data Transformation Stage"
STAGE_NAME4 = "Model Trainer Stage"

if __name__ == "__main__":
    try:
        logger.info(f">>>>>> Stage {STAGE_NAME1} started <<<<<<")
        data_ingestion = DataIngestionTrainingPipeline()
        data_ingestion.initiate_data_ingestion()
        logger.info(f">>>>>> Stage {STAGE_NAME1} completed <<<<<<\n\nx==========x")

        
        logger.info(f">>>>>> Stage {STAGE_NAME2} started <<<<<<")
        data_validation = DataValidationTrainingPipeline()
        data_validation.initiate_data_validation()
        logger.info(f">>>>>> Stage {STAGE_NAME2} completed <<<<<<\n\nx==========x")
        logger.info(f">>>>>> Stage {STAGE_NAME3} started <<<<<<")
        data_transformation = DataTransformationTrainingPipeline()
        data_transformation.initiate_data_transformation()
        logger.info(f">>>>>> Stage {STAGE_NAME3} completed <<<<<<\n\nx==========x")

        logger.info(f">>>>>> Stage {STAGE_NAME4} started <<<<<<")
        model_trainer = ModelTrainerTrainingPipeline()
        model_trainer.initiate_model_trainer()
        logger.info(f">>>>>> Stage {STAGE_NAME4} completed <<<<<<\n\nx==========x")

    except Exception as e:
        logger.exception(e)
        raise e

