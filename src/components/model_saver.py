import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import joblib
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier
from src.utils.logger import logger
from src.utils.exception import CustomException


@dataclass
class ModelSaverConfig:
    """
    Configuration dataclass for Model Saver component.
    Defines artifact input paths and saved model output destination.
    """
    X_train_path: str = os.path.join("artifacts", "X_train.csv")
    y_train_path: str = os.path.join("artifacts", "y_train.csv")
    model_output_path: str = os.path.join("artifacts", "best_model.joblib")
    preprocessor_path: str = os.path.join("artifacts", "preprocessor.joblib")


class ModelSaver:
    """
    Model Saver component responsible for fitting the champion Gradient Boosting model
    on the full training dataset and persisting the serialized model artifact using Joblib.
    """

    def __init__(self, config: ModelSaverConfig = ModelSaverConfig()):
        self.config = config
        os.makedirs(os.path.dirname(self.config.model_output_path), exist_ok=True)

    def train_and_save_champion_model(self) -> str:
        """
        Trains the champion Gradient Boosting Classifier on preprocessed X_train/y_train
        and serializes it to artifacts/best_model.joblib.
        """
        logger.info("Initiating Model Saver Component...")
        try:
            # 1. Verify preprocessor exists
            if not os.path.exists(self.config.preprocessor_path):
                raise FileNotFoundError(f"Preprocessor artifact missing at: {self.config.preprocessor_path}")

            logger.info(f"Verified Preprocessor object at: {self.config.preprocessor_path}")

            # 2. Load preprocessed training artifacts
            logger.info("Loading preprocessed training features and labels...")
            X_train = pd.read_csv(self.config.X_train_path)
            y_train = pd.read_csv(self.config.y_train_path).squeeze("columns")

            # 3. Fit Champion Gradient Boosting Model
            logger.info("Fitting Champion Gradient Boosting Model...")
            champion_model = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=3,
                random_state=42
            )
            champion_model.fit(X_train, y_train)

            # 4. Serialize model binary using Joblib
            logger.info(f"Serializing champion model to: {self.config.model_output_path}...")
            joblib.dump(champion_model, self.config.model_output_path)

            # 5. Verify model binary loads successfully
            loaded_model = joblib.load(self.config.model_output_path)
            logger.info("Model verification check PASSED successfully.")

            logger.info("Model Saver Component completed successfully.")
            return self.config.model_output_path

        except Exception as e:
            logger.error("Failed to train and save champion model!")
            raise CustomException(e, sys)


if __name__ == "__main__":
    try:
        saver = ModelSaver()
        saved_path = saver.train_and_save_champion_model()
        print(f"\nModel Serialization Complete! Saved to: {saved_path}")
    except Exception as e:
        print(f"Model Saver Failed: {e}")
