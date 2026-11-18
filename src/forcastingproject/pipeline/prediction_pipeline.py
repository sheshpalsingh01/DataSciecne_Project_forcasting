import argparse
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from datetime import date
from math import isfinite
from pathlib import Path

import joblib
import pandas as pd

from src.forcastingproject.constants import CONFIG_FILE_PATH
from src.forcastingproject.utils.common import read_yaml_file


@dataclass(frozen=True)
class CustomData:
    Store: int
    Date: str
    Open: int
    Promo: int
    StateHoliday: str | int
    SchoolHoliday: int
    StoreType: str
    Assortment: str
    Promo2: int
    CompetitionDistance: float | None = None
    CompetitionOpenSinceMonth: int | None = None
    CompetitionOpenSinceYear: int | None = None
    Promo2SinceWeek: int | None = None
    Promo2SinceYear: int | None = None
    PromoInterval: str | None = None

    def get_data_as_data_frame(self) -> pd.DataFrame:
        try:
            sale_date = date.fromisoformat(self.Date)
        except (TypeError, ValueError) as exc:
            raise ValueError("Date must be an ISO date such as 2015-07-31.") from exc

        row = asdict(self)
        del row["Date"]
        store = self._number("Store", self.Store)
        if store < 1 or not store.is_integer():
            raise ValueError("Store must be a positive integer.")
        row["Store"] = int(store)

        for field in ("Open", "Promo", "SchoolHoliday", "Promo2"):
            value = self._number(field, row[field])
            if value not in (0, 1):
                raise ValueError(f"{field} must be 0 or 1.")
            row[field] = int(value)

        for field in ("StoreType", "Assortment"):
            value = row[field]
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field} must be a non-empty string.")
            row[field] = value.strip()

        if self.StateHoliday == 0:
            row["StateHoliday"] = "0"
        elif isinstance(self.StateHoliday, str) and self.StateHoliday.strip():
            row["StateHoliday"] = self.StateHoliday.strip()
        else:
            raise ValueError("StateHoliday must be 0 or a non-empty string.")

        if self.CompetitionDistance is None:
            row["CompetitionDistance"] = float("nan")
        else:
            row["CompetitionDistance"] = self._number("CompetitionDistance", self.CompetitionDistance)

        for field in (
            "CompetitionOpenSinceMonth",
            "CompetitionOpenSinceYear",
            "Promo2SinceWeek",
            "Promo2SinceYear",
        ):
            value = 0.0 if row[field] is None else self._number(field, row[field])
            if not value.is_integer():
                raise ValueError(f"{field} must be an integer.")
            row[field] = int(value)

        if self.PromoInterval is not None and not isinstance(self.PromoInterval, str):
            raise ValueError("PromoInterval must be a string or null.")
        row["PromoInterval"] = (self.PromoInterval or "").strip() or "None"

        row.update(
            Year=sale_date.year,
            Month=sale_date.month,
            Day=sale_date.day,
            DayOfWeek=sale_date.weekday(),
            WeekOfYear=sale_date.isocalendar().week,
        )
        return pd.DataFrame([row])

    @staticmethod
    def _number(field: str, value: object) -> float:
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{field} must be a finite non-negative number.") from exc
        if not isfinite(number) or number < 0:
            raise ValueError(f"{field} must be a finite non-negative number.")
        return number


class PredictionPipeline:
    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH):
        config = read_yaml_file(config_file_path)
        transformation_dir = Path(config.data_transformation.root_dir)
        trainer = config.model_trainer

        self.preprocessor = self._load_artifact(
            transformation_dir / "preprocessor.joblib", "Stage 03 data transformation"
        )
        self.model = self._load_artifact(
            Path(trainer.root_dir) / trainer.model_name, "Stage 04 model training"
        )
        self.feature_names = self.preprocessor.get_feature_names_out()

    def predict(self, payload: Mapping[str, object] | CustomData) -> float:
        data = payload if isinstance(payload, CustomData) else CustomData(**payload)
        features = data.get_data_as_data_frame()
        transformed = self.preprocessor.transform(features)
        model_input = pd.DataFrame(transformed, columns=self.feature_names)
        return float(self.model.predict(model_input)[0])

    @staticmethod
    def _load_artifact(path: Path, stage: str):
        try:
            return joblib.load(path)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Missing prediction artifact at {path}. Fetch it with dvc pull or run {stage}."
            ) from exc


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict daily sales for one store.")
    parser.add_argument("payload", help="JSON object containing the store and date features.")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)
        if not isinstance(payload, dict):
            raise ValueError("The payload must be a JSON object.")
        prediction = PredictionPipeline().predict(payload)
    except (TypeError, ValueError, FileNotFoundError) as exc:
        parser.error(str(exc))

    print(prediction)
