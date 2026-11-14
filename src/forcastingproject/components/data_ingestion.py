import os
import sys
import shutil
import pandas as pd
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.exception.exception import CustomException
from src.forcastingproject.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_data(self):
        """
        Copies raw train and store datasets into the data_ingestion artifacts directory.
        """
        try:
            logger.info("Starting data download/copy process...")
            raw_train_path = os.path.join(self.config.root_dir, "train.csv")
            raw_store_path = os.path.join(self.config.root_dir, "store.csv")

            if not os.path.exists(raw_train_path):
                shutil.copy(self.config.train_data, raw_train_path)
                logger.info(f"Copied {self.config.train_data} to {raw_train_path}")
            else:
                logger.info(f"File {raw_train_path} already exists.")

            if not os.path.exists(raw_store_path):
                shutil.copy(self.config.store_data, raw_store_path)
                logger.info(f"Copied {self.config.store_data} to {raw_store_path}")
            else:
                logger.info(f"File {raw_store_path} already exists.")

        except Exception as e:
            raise CustomException(e, sys)

    def merge_data(self) -> pd.DataFrame:
        """
        Merges train.csv and store.csv on Store column and saves as raw.csv in root_dir.
        """
        try:
            logger.info("Starting data merge process...")
            train_df = pd.read_csv(self.config.train_data, low_memory=False)
            store_df = pd.read_csv(self.config.store_data, low_memory=False)

            logger.info(f"Train data shape: {train_df.shape}")
            logger.info(f"Store data shape: {store_df.shape}")

            merged_df = pd.merge(train_df, store_df, on="Store", how="left")
            logger.info(f"Merged data shape: {merged_df.shape}")

            merged_data_path = os.path.join(self.config.root_dir, "raw.csv")
            merged_df.to_csv(merged_data_path, index=False)
            logger.info(f"Merged raw data saved at {merged_data_path}")

            return merged_df
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        """
        Executes the full data ingestion pipeline: copies source files and merges them.
        """
        try:
            self.download_data()
            merged_df = self.merge_data()
            logger.info("Data Ingestion completed successfully.")
            return merged_df
        except Exception as e:
            raise CustomException(e, sys)

