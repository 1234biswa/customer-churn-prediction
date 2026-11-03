import os
import sys
import time
sys.path.append(os.getcwd())

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from src.utils.logger import logger
from src.utils.exception import CustomException

# Set Seaborn plot theme
sns.set_theme(style="whitegrid")


@dataclass
class ModelEvaluationConfig:
    """
    Configuration dataclass for Model Evaluation component.
    Defines artifact paths and output figure directory.
    """
    X_train_path: str = os.path.join("artifacts", "X_train.csv")
    X_test_path: str = os.path.join("artifacts", "X_test.csv")
    y_train_path: str = os.path.join("artifacts", "y_train.csv")
    y_test_path: str = os.path.join("artifacts", "y_test.csv")
    figures_dir: str = os.path.join("reports", "figures")


class ModelEvaluator:
    """
    Model Evaluator component responsible for performing comprehensive metric evaluation,
    confusion matrix rendering, feature importance extraction, error analysis, and candidate comparison.
    """

    def __init__(self, config: ModelEvaluationConfig = ModelEvaluationConfig()):
        self.config = config
        os.makedirs(self.config.figures_dir, exist_ok=True)

    def load_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Loads artifacts from artifacts directory."""
        try:
            logger.info("Loading preprocessed dataset splits for evaluation...")
            X_train = pd.read_csv(self.config.X_train_path)
            X_test = pd.read_csv(self.config.X_test_path)
            y_train = pd.read_csv(self.config.y_train_path).squeeze("columns")
            y_test = pd.read_csv(self.config.y_test_path).squeeze("columns")
            return X_train, X_test, y_train, y_test
        except Exception as e:
            logger.error("Failed to load preprocessed data for evaluation!")
            raise CustomException(e, sys)

    def evaluate_all_models(
        self, X_train: pd.DataFrame, X_test: pd.DataFrame, y_train: pd.Series, y_test: pd.Series
    ) -> tuple[pd.DataFrame, dict, dict]:
        """
        Fits candidate models, measures train and predict times, computes metrics and confusion matrices.
        """
        try:
            logger.info("Evaluating Candidate Machine Learning Models...")
            models = {
                "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
                "Decision Tree": DecisionTreeClassifier(max_depth=6, random_state=42),
                "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
                "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
                "XGBoost": XGBClassifier(n_estimators=100, eval_metric="logloss", random_state=42)
            }

            eval_results = []
            confusion_matrices = {}
            trained_models = {}

            for name, model in models.items():
                logger.info(f"Measuring performance for {name}...")

                # Measure Training Time
                start_train = time.time()
                model.fit(X_train, y_train)
                train_time = (time.time() - start_train) * 1000  # ms

                # Measure Prediction Time
                start_pred = time.time()
                y_pred = model.predict(X_test)
                pred_time = (time.time() - start_pred) * 1000  # ms

                y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else y_pred

                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, zero_division=0)
                rec = recall_score(y_test, y_pred, zero_division=0)
                f1 = f1_score(y_test, y_pred, zero_division=0)
                roc_auc = roc_auc_score(y_test, y_proba)

                cm = confusion_matrix(y_test, y_pred)
                confusion_matrices[name] = cm
                trained_models[name] = model

                eval_results.append({
                    "Model Name": name,
                    "Accuracy": acc,
                    "Precision": prec,
                    "Recall": rec,
                    "F1 Score": f1,
                    "ROC-AUC": roc_auc,
                    "Train Time (ms)": round(train_time, 2),
                    "Pred Time (ms)": round(pred_time, 2)
                })

            eval_df = pd.DataFrame(eval_results).sort_values(by="ROC-AUC", ascending=False).reset_index(drop=True)
            return eval_df, confusion_matrices, trained_models

        except Exception as e:
            logger.error("Error evaluating candidate models!")
            raise CustomException(e, sys)

    def plot_confusion_matrices(self, confusion_matrices: dict):
        """Plots 2x3 grid of confusion matrices for all models."""
        try:
            logger.info("Plotting Confusion Matrices Grid...")
            fig, axes = plt.subplots(2, 3, figsize=(16, 10))
            axes = axes.flatten()

            for idx, (name, cm) in enumerate(confusion_matrices.items()):
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=axes[idx],
                            xticklabels=["Retained (0)", "Churned (1)"],
                            yticklabels=["Retained (0)", "Churned (1)"])
                axes[idx].set_title(f"{name}\nConfusion Matrix", fontweight="bold")
                axes[idx].set_ylabel("Actual Label")
                axes[idx].set_xlabel("Predicted Label")

            # Remove empty 6th subplot
            fig.delaxes(axes[5])

            plt.tight_layout()
            save_path = os.path.join(self.config.figures_dir, "12_confusion_matrices.png")
            plt.savefig(save_path, dpi=300)
            plt.close()
            logger.info(f"Saved Confusion Matrices plot to: {save_path}")

        except Exception as e:
            logger.error("Error plotting confusion matrices!")
            raise CustomException(e, sys)

    def plot_feature_importance(self, model, feature_names: list[str]) -> pd.DataFrame:
        """Extracts and plots Top 20 Feature Importances from Gradient Boosting model."""
        try:
            logger.info("Extracting Feature Importance for Gradient Boosting model...")
            importances = model.feature_importances_
            feature_imp_df = pd.DataFrame({
                "Feature": feature_names,
                "Importance": importances
            }).sort_values(by="Importance", ascending=False).reset_index(drop=True)

            top20 = feature_imp_df.head(20)

            plt.figure(figsize=(12, 8))
            sns.barplot(data=top20, x="Importance", y="Feature", hue="Feature", palette="viridis", legend=False)
            plt.title("Top 20 Feature Importance (Gradient Boosting)", fontsize=14, fontweight="bold")
            plt.xlabel("Gini Importance Score")
            plt.ylabel("Engineered & Preprocessed Feature")
            plt.tight_layout()

            save_path = os.path.join(self.config.figures_dir, "13_feature_importance.png")
            plt.savefig(save_path, dpi=300)
            plt.close()

            logger.info(f"Saved Feature Importance plot to: {save_path}")
            return top20

        except Exception as e:
            logger.error("Error plotting feature importances!")
            raise CustomException(e, sys)

    def initiate_evaluation(self) -> dict:
        """Main evaluation orchestration method."""
        logger.info("Initiating Comprehensive Model Evaluation Component...")
        X_train, X_test, y_train, y_test = self.load_data()
        eval_df, confusion_matrices, trained_models = self.evaluate_all_models(X_train, X_test, y_train, y_test)
        self.plot_confusion_matrices(confusion_matrices)

        best_model_name = "Gradient Boosting"  # Best balance of F1, Accuracy, and ROC-AUC
        top20_df = self.plot_feature_importance(trained_models[best_model_name], list(X_train.columns))

        best_row = eval_df[eval_df["Model Name"] == best_model_name].iloc[0]

        logger.info("Model Evaluation Component Completed Successfully.")
        return {
            "eval_df": eval_df,
            "best_model_name": best_model_name,
            "best_accuracy": best_row["Accuracy"],
            "best_roc_auc": best_row["ROC-AUC"],
            "best_f1": best_row["F1 Score"],
            "best_recall": best_row["Recall"],
            "best_precision": best_row["Precision"],
            "top20_features": top20_df
        }


if __name__ == "__main__":
    try:
        evaluator = ModelEvaluator()
        out = evaluator.initiate_evaluation()
        print("\n" + "="*80)
        print("                     COMPREHENSIVE MODEL EVALUATION REPORT")
        print("="*80)
        print(out["eval_df"].to_string(index=False))
        print("="*80)
        print(f"\nCHAMPION MODEL SELECTED: {out['best_model_name']}")
        print(f"• Accuracy:  {out['best_accuracy']:.4f}")
        print(f"• ROC-AUC:   {out['best_roc_auc']:.4f}")
        print(f"• F1-Score:  {out['best_f1']:.4f}")
        print(f"• Recall:    {out['best_recall']:.4f}")
        print(f"• Precision: {out['best_precision']:.4f}")
        print("="*80)
    except Exception as e:
        print(f"Model Evaluation Failed: {e}")
