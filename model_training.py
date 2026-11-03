import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from src.utils.logger import logger
from src.utils.exception import CustomException

# Set Seaborn plot aesthetics
sns.set_theme(style="whitegrid")


@dataclass
class ModelTrainerConfig:
    """
    Configuration dataclass for Model Training component.
    Defines paths for train/test data splits and figure outputs.
    """
    X_train_path: str = os.path.join("artifacts", "X_train.csv")
    X_test_path: str = os.path.join("artifacts", "X_test.csv")
    y_train_path: str = os.path.join("artifacts", "y_train.csv")
    y_test_path: str = os.path.join("artifacts", "y_test.csv")
    figures_dir: str = os.path.join("reports", "figures")


class ModelTrainer:
    """
    Model Training component responsible for initializing, training,
    evaluating, and comparing multiple machine learning classification algorithms.
    """

    def __init__(self, config: ModelTrainerConfig = ModelTrainerConfig()):
        self.config = config
        os.makedirs(self.config.figures_dir, exist_ok=True)

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Loads preprocessed training and testing artifacts."""
        try:
            logger.info("Loading Preprocessed Artifacts from artifacts/...")
            X_train = pd.read_csv(self.config.X_train_path)
            X_test = pd.read_csv(self.config.X_test_path)
            y_train = pd.read_csv(self.config.y_train_path).squeeze("columns")
            y_test = pd.read_csv(self.config.y_test_path).squeeze("columns")
            logger.info(f"Loaded X_train: {X_train.shape}, X_test: {X_test.shape}")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error("Failed to load artifacts for model training!")
            raise CustomException(e, sys)

    def get_models(self) -> dict:
        """Initializes dictionary of classification algorithms."""
        models = {
            "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
            "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
            "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
        }
        if XGBOOST_AVAILABLE:
            models["XGBoost"] = XGBClassifier(
                n_estimators=100, eval_metric="logloss", random_state=42
            )
        else:
            logger.warning("XGBoost is not installed. Skipping XGBoost model.")
        return models

    def train_and_evaluate(
        self, models: dict, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series
    ) -> pd.DataFrame:
        """
        Trains each classifier on training data and computes evaluation metrics on test set.
        """
        try:
            logger.info("Starting Model Training & Evaluation Phase...")
            results = []
            self.curves_data = {}

            for name, model in models.items():
                logger.info(f"Training {name} Classifier...")
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                if hasattr(model, "predict_proba"):
                    y_proba = model.predict_proba(X_test)[:, 1]
                else:
                    y_proba = y_pred

                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, zero_division=0)
                rec = recall_score(y_test, y_pred, zero_division=0)
                f1 = f1_score(y_test, y_pred, zero_division=0)
                roc_auc = roc_auc_score(y_test, y_proba)

                results.append({
                    "Model Name": name,
                    "Accuracy": acc,
                    "Precision": prec,
                    "Recall": rec,
                    "F1 Score": f1,
                    "ROC-AUC": roc_auc
                })

                # Store curves data for plotting
                fpr, tpr, _ = roc_curve(y_test, y_proba)
                prec_curve, rec_curve, _ = precision_recall_curve(y_test, y_proba)
                self.curves_data[name] = {
                    "fpr": fpr, "tpr": tpr,
                    "prec_curve": prec_curve, "rec_curve": rec_curve,
                    "roc_auc": roc_auc
                }

                logger.info(f"Completed {name} -> ROC-AUC: {roc_auc:.4f}, Accuracy: {acc:.4f}, F1: {f1:.4f}")

            results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
            return results_df

        except Exception as e:
            logger.error("Error during model training and evaluation!")
            raise CustomException(e, sys)

    def generate_visualizations(self, results_df: pd.DataFrame):
        """Generates Model Comparison Bar Chart, ROC Curves, and Precision-Recall Curves."""
        try:
            logger.info("Generating Model Comparison Charts...")

            # 1. Model Comparison Bar Chart
            plt.figure(figsize=(12, 6))
            df_melted = pd.melt(results_df, id_vars=["Model Name"], var_name="Metric", value_name="Score")
            sns.barplot(data=df_melted, x="Model Name", y="Score", hue="Metric", palette="Set2")
            plt.title("Classification Metrics Comparison Across Models", fontsize=14, fontweight="bold")
            plt.ylim(0.0, 1.05)
            plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
            plt.tight_layout()
            path1 = os.path.join(self.config.figures_dir, "09_model_comparison.png")
            plt.savefig(path1, dpi=300)
            plt.close()

            # 2. ROC Curves Plot
            plt.figure(figsize=(9, 7))
            for name, data in self.curves_data.items():
                plt.plot(data["fpr"], data["tpr"], label=f"{name} (AUC = {data['roc_auc']:.3f})", linewidth=2)
            plt.plot([0, 1], [0, 1], "k--", label="Random Classifier (AUC = 0.500)")
            plt.xlabel("False Positive Rate (1 - Specificity)")
            plt.ylabel("True Positive Rate (Recall)")
            plt.title("Receiver Operating Characteristic (ROC) Curves", fontsize=14, fontweight="bold")
            plt.legend(loc="lower right")
            plt.tight_layout()
            path2 = os.path.join(self.config.figures_dir, "10_roc_curves.png")
            plt.savefig(path2, dpi=300)
            plt.close()

            # 3. Precision-Recall Curves Plot
            plt.figure(figsize=(9, 7))
            for name, data in self.curves_data.items():
                plt.plot(data["rec_curve"], data["prec_curve"], label=f"{name}", linewidth=2)
            plt.xlabel("Recall")
            plt.ylabel("Precision")
            plt.title("Precision-Recall Curves", fontsize=14, fontweight="bold")
            plt.legend(loc="lower left")
            plt.tight_layout()
            path3 = os.path.join(self.config.figures_dir, "11_precision_recall_curves.png")
            plt.savefig(path3, dpi=300)
            plt.close()

            logger.info("All comparison charts successfully saved in reports/figures/")

        except Exception as e:
            logger.error("Error generating comparison visualizations!")
            raise CustomException(e, sys)

    def initiate_model_training(self) -> pd.DataFrame:
        """Main orchestration method for model training and comparison."""
        logger.info("Initiating Model Training Component...")
        X_train, X_test, y_train, y_test = self.load_data()
        models = self.get_models()
        results_df = self.train_and_evaluate(models, X_train, X_test, y_train, y_test)
        self.generate_visualizations(results_df)

        logger.info("Model Training Phase Completed Successfully.")
        return results_df


if __name__ == "__main__":
    try:
        trainer = ModelTrainer()
        results = trainer.initiate_model_training()
        print("\n" + "="*70)
        print("                 MODEL PERFORMANCE COMPARISON TABLE")
        print("="*70)
        print(results.to_string(index=False))
        print("="*70)
    except Exception as e:
        print(f"Model Training Failed: {e}")
