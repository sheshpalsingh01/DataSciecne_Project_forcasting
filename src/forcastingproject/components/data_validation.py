import os
import sys
import shutil
import pandas as pd
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.exception.exception import CustomException
from src.forcastingproject.entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validation_all_columns(self) -> bool:
        try:
            validation_status = True
            data = pd.read_csv(self.config.data_file_dir, low_memory=False)
            all_cols = list(data.columns)
            all_schema = list(self.config.all_schema.keys())

            for col in all_cols:
                if col not in all_schema:
                    validation_status = False
                    break

            with open(self.config.status_file, "w") as f:
                f.write(f"Validation status: {validation_status}\n")

            return validation_status
        except Exception as e:
            raise CustomException(e, sys)

    def get_dataframe(self) -> pd.DataFrame:
        try:
            return pd.read_csv(self.config.data_file_dir, low_memory=False)
        except Exception as e:
            raise CustomException(e, sys)

    @staticmethod
    def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
        try:
            data = df.copy()

            # 1. CompetitionDistance -> median
            data["CompetitionDistance"] = data["CompetitionDistance"].fillna(
                data["CompetitionDistance"].median()
            )

            # 2. Competition open dates -> 0 (unknown)
            data["CompetitionOpenSinceMonth"] = (
                data["CompetitionOpenSinceMonth"].fillna(0).astype(int)
            )
            data["CompetitionOpenSinceYear"] = (
                data["CompetitionOpenSinceYear"].fillna(0).astype(int)
            )

            # 3. Promo2 features -> 0 / "None"
            data["Promo2SinceWeek"] = data["Promo2SinceWeek"].fillna(0).astype(int)
            data["Promo2SinceYear"] = data["Promo2SinceYear"].fillna(0).astype(int)
            data["PromoInterval"] = data["PromoInterval"].fillna("None")

            return data
        except Exception as e:
            raise CustomException(e, sys)
