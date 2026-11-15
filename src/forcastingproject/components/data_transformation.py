import os
import sys
import joblib
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from src.forcastingproject.logging.logger import logger
from src.forcastingproject.exception.exception import CustomException
from src.forcastingproject.entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def _save_plot(self, name: str):
        os.makedirs(self.config.reports_dir, exist_ok=True)
        path = os.path.join(self.config.reports_dir, name)
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved plot: {path}")

    def _load_data(self) -> pd.DataFrame:
        data_path = self.config.data_path
        df = pd.read_csv(data_path)
        logger.info(f"Loaded data from {data_path} with shape {df.shape}")
        return df

    def _add_date_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df["Year"] = df["Date"].dt.year
        df["Month"] = df["Date"].dt.month
        df["Day"] = df["Date"].dt.day
        df["DayOfWeek"] = df["Date"].dt.dayofweek
        df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
        return df

    def explor_data_analysis(self):
        try:
            df = self._add_date_features(self._load_data())
            df["PromoInterval"] = df["PromoInterval"].fillna("")

            monthly_sales = df.groupby(["Year", "Month"], as_index=False)["Sales"].sum()
            monthly_sales["Date"] = pd.to_datetime(monthly_sales[["Year", "Month"]].assign(DAY=1))
            plt.figure(figsize=(14, 6))
            sns.lineplot(data=monthly_sales, x="Date", y="Sales")
            plt.title("Total Sales Over Time (Monthly)")
            plt.xlabel("Month")
            plt.ylabel("Sales")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            self._save_plot("monthly_sales_trend.png")

            top_stores = df.groupby("Store")["Sales"].sum().sort_values(ascending=False).head(10)
            plt.figure(figsize=(10, 5))
            sns.barplot(x=top_stores.index.astype(str), y=top_stores.values, palette="viridis")
            plt.title("Top 10 Stores by Total Sales")
            plt.xlabel("Store ID")
            plt.ylabel("Total Sales")
            plt.tight_layout()
            self._save_plot("top10_stores.png")

            dow_sales = df.groupby("DayOfWeek")["Sales"].mean().sort_index()
            plt.figure(figsize=(8, 5))
            sns.barplot(x=dow_sales.index, y=dow_sales.values, palette="magma")
            plt.title("Average Sales by Day of the Week (0=Mon)")
            plt.xlabel("Day of Week")
            plt.ylabel("Average Sales")
            plt.tight_layout()
            self._save_plot("sales_by_dayofweek.png")

            plt.figure(figsize=(6, 4))
            sns.barplot(x="Promo", y="Sales", data=df, palette="coolwarm")
            plt.title("Sales: Promo vs No Promo")
            plt.xlabel("Promo (0 = No, 1 = Yes)")
            plt.ylabel("Sales")
            plt.tight_layout()
            self._save_plot("promo_vs_sales.png")

            logger.info("EDA completed and plots saved")
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):
        try:
            df = self._add_date_features(self._load_data())

            # Domain-specific missing value imputation
            if "CompetitionDistance" in df.columns:
                df["CompetitionDistance"] = df["CompetitionDistance"].fillna(df["CompetitionDistance"].median())
            for col in ["CompetitionOpenSinceMonth", "CompetitionOpenSinceYear", "Promo2SinceWeek", "Promo2SinceYear"]:
                if col in df.columns:
                    df[col] = df[col].fillna(0)
            if "PromoInterval" in df.columns:
                df["PromoInterval"] = df["PromoInterval"].fillna("None")

            # Feature selection: drop target and non-predictive/unavailable-at-forecast-time columns
            drop_cols = [c for c in ["Sales", "Date", "Customers"] if c in df.columns]
            target_col = "Sales"

            
            if target_col not in df.columns:
                raise ValueError("Target column 'Sales' not found in data")

            X = df.drop(columns=drop_cols)
            y = df[target_col]

            categorical_features = [c for c in ["StoreType", "Assortment", "StateHoliday", "PromoInterval"] if c in X.columns]
            numeric_features = [c for c in X.columns if c not in categorical_features]
            for col in categorical_features:
                X[col] = X[col].astype(str)


            numeric_transformer = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="median")),
            ])
            categorical_transformer = Pipeline(steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ])

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", numeric_transformer, numeric_features),
                    ("cat", categorical_transformer, categorical_features),
                ],
                remainder="drop",
            )

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            X_train_arr = preprocessor.fit_transform(X_train)
            X_test_arr = preprocessor.transform(X_test)

            feature_names = preprocessor.get_feature_names_out()
            train_df = pd.DataFrame(X_train_arr, columns=feature_names)
            train_df["Sales"] = y_train.reset_index(drop=True).values
            test_df = pd.DataFrame(X_test_arr, columns=feature_names)
            test_df["Sales"] = y_test.reset_index(drop=True).values

            os.makedirs(self.config.root_dir, exist_ok=True)
            train_path = os.path.join(self.config.root_dir, "train.csv")
            test_path = os.path.join(self.config.root_dir, "test.csv")
            preprocessor_path = os.path.join(self.config.root_dir, "preprocessor.joblib")

            train_df.to_csv(train_path, index=False)
            test_df.to_csv(test_path, index=False)
            joblib.dump(preprocessor, preprocessor_path)

            logger.info(f"Saved train data to {train_path} with shape {train_df.shape}")
            logger.info(f"Saved test data to {test_path} with shape {test_df.shape}")
            logger.info(f"Saved preprocessor to {preprocessor_path}")
            print("Train shape:", train_df.shape)
            print("Test shape:", test_df.shape)
            print("Preprocessor saved to:", preprocessor_path)

            return train_path, test_path, preprocessor_path
        except Exception as e:
            raise CustomException(e, sys)