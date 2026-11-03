import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import joblib
from dataclasses import dataclass

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split

from src.utils.logger import logger
from src.utils.exception import CustomException
from src.components.feature_engineering import FeatureEngineer


@dataclass
class DataPreprocessingConfig:
    """
    Configuration dataclass for Data Preprocessing component.
    Defines paths for saving preprocessor binaries and processed dataset splits.
    """
    cleaned_data_path: str = os.path.join("data", "processed", "cleaned_telco_customer_churn.csv")
    artifacts_dir: str = "artifacts"
    preprocessor_obj_path: str = os.path.join("artifacts", "preprocessor.joblib")
    X_train_path: str = os.path.join("artifacts", "X_train.csv")
    X_test_path: str = os.path.join("artifacts", "X_test.csv")
    y_train_path: str = os.path.join("artifacts", "y_train.csv")
    y_test_path: str = os.path.join("artifacts", "y_test.csv")
    test_size: float = 0.2
    random_state: int = 42


class DataPreprocessor:
    """
    Data Preprocessing component responsible for feature selection, target encoding,
    building Scikit-Learn pipelines, column transformations, train-test splitting,
    and persisting artifact files.
    """

    def __init__(self, config: DataPreprocessingConfig = DataPreprocessingConfig()):
        self.config = config
        os.makedirs(self.config.artifacts_dir, exist_ok=True)

    def get_data_transformer_object(
        self, numerical_features: list[str], categorical_features: list[str]
    ) -> ColumnTransformer:
        """
        Constructs a Scikit-Learn ColumnTransformer pipeline:
        - Numerical Pipeline: SimpleImputer (median) + StandardScaler
        - Categorical Pipeline: SimpleImputer (most_frequent) + OneHotEncoder (drop='first', handle_unknown='ignore')
        """
        try:
            logger.info("Building ColumnTransformer preprocessing pipeline...")

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_features),
                    ("cat_pipeline", cat_pipeline, categorical_features),
                ]
            )

            logger.info("Pipeline creation completed.")
            return preprocessor

        except Exception as e:
            logger.error("Error creating data transformer object!")
            raise CustomException(e, sys)

    def initiate_data_preprocessing(self) -> dict:
        """
        Full orchestration of data loading, feature engineering, target encoding,
        column transformation, stratified train-test splitting, and artifact saving.
        """
        logger.info("Initiating Data Preprocessing Component...")
        try:
            # 1. Load cleaned dataset
            if not os.path.exists(self.config.cleaned_data_path):
                raise FileNotFoundError(f"Cleaned dataset not found at: {self.config.cleaned_data_path}")

            logger.info(f"Loading cleaned data from: {self.config.cleaned_data_path}")
            df = pd.read_csv(self.config.cleaned_data_path)

            # 2. Apply Feature Engineering
            fe = FeatureEngineer()
            df_fe = fe.transform_features(df)

            # 3. Feature Selection & Drop Non-Predictive Column (customerID)
            logger.info("Dropping non-predictive primary key: 'customerID'")
            if "customerID" in df_fe.columns:
                df_fe.drop(columns=["customerID"], inplace=True)

            # 4. Separate Input Features (X) and Target (y)
            target_column = "Churn"
            X = df_fe.drop(columns=[target_column])
            y_raw = df_fe[target_column]

            # 5. Encode Target Variable (Yes -> 1, No -> 0)
            logger.info("Encoding Target Variable 'Churn': Yes -> 1, No -> 0...")
            y = y_raw.map({"Yes": 1, "No": 0})

            # 6. Identify Numerical and Categorical Features
            numerical_features = list(X.select_dtypes(include=["int64", "float64"]).columns)
            categorical_features = list(X.select_dtypes(include=["object", "category", "string"]).columns)

            logger.info(f"Numerical Features ({len(numerical_features)}): {numerical_features}")
            logger.info(f"Categorical Features ({len(categorical_features)}): {categorical_features}")

            # 7. Stratified Train-Test Split (80% Train, 20% Test)
            logger.info("Splitting dataset (80% Train / 20% Test) with Stratified Sampling...")
            X_train_raw, X_test_raw, y_train, y_test = train_test_split(
                X,
                y,
                test_size=self.config.test_size,
                random_state=self.config.random_state,
                stratify=y
            )

            # 8. Obtain ColumnTransformer & Fit on Train Set
            preprocessor_obj = self.get_data_transformer_object(numerical_features, categorical_features)
            logger.info("Fitting preprocessor pipeline on training features...")
            
            X_train_arr = preprocessor_obj.fit_transform(X_train_raw)
            X_test_arr = preprocessor_obj.transform(X_test_raw)

            # Retrieve transformed encoded feature names
            cat_encoder = preprocessor_obj.named_transformers_["cat_pipeline"].named_steps["one_hot_encoder"]
            encoded_cat_names = list(cat_encoder.get_feature_names_out(categorical_features))
            all_feature_names = numerical_features + encoded_cat_names

            # 9. Convert numpy arrays back to DataFrames for CSV saving
            X_train_df = pd.DataFrame(X_train_arr, columns=all_feature_names)
            X_test_df = pd.DataFrame(X_test_arr, columns=all_feature_names)

            # 10. Save Artifacts inside artifacts/ folder
            logger.info("Saving Preprocessing Artifacts...")
            joblib.dump(preprocessor_obj, self.config.preprocessor_obj_path)
            X_train_df.to_csv(self.config.X_train_path, index=False)
            X_test_df.to_csv(self.config.X_test_path, index=False)
            y_train.to_csv(self.config.y_train_path, index=False)
            y_test.to_csv(self.config.y_test_path, index=False)

            logger.info(f"Saved preprocessor binary to: {self.config.preprocessor_obj_path}")
            logger.info(f"Saved X_train to: {self.config.X_train_path} Shape: {X_train_df.shape}")
            logger.info(f"Saved X_test to:  {self.config.X_test_path} Shape: {X_test_df.shape}")
            logger.info("Data Preprocessing Component Completed Successfully!")

            return {
                "raw_features_count": X.shape[1],
                "encoded_features_count": len(all_feature_names),
                "train_samples": len(X_train_df),
                "test_samples": len(X_test_df),
                "preprocessor_path": self.config.preprocessor_obj_path,
                "feature_names": all_feature_names
            }

        except Exception as e:
            logger.error("Error during Data Preprocessing execution!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        preprocessor = DataPreprocessor()
        summary = preprocessor.initiate_data_preprocessing()
        print("\n" + "="*50)
        print("         DATA PREPROCESSING SUMMARY OUTPUT")
        print("="*50)
        print(f"• Raw Features Count:     {summary['raw_features_count']}")
        print(f"• Encoded Features Count: {summary['encoded_features_count']}")
        print(f"• Training Samples:       {summary['train_samples']} rows")
        print(f"• Testing Samples:        {summary['test_samples']} rows")
        print(f"• Saved Preprocessor:     {summary['preprocessor_path']}")
        print("="*50)
    except Exception as e:
        print(f"Data Preprocessing Pipeline Failed: {e}")
