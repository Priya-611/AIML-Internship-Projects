"""Train an XGBoost fraud classifier and save it for the API."""
import argparse
import json
from pathlib import Path

import joblib
import mlflow
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    average_precision_score, classification_report,
    confusion_matrix, precision_score, recall_score, f1_score
)
from xgboost import XGBClassifier

from src.preprocessing import load_dataset, split_features_target

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=str(ROOT / "dataset" / "creditcard.csv"))
    parser.add_argument("--model-out", default=str(ROOT / "models" / "fraud_model.joblib"))
    args = parser.parse_args()

    df = load_dataset(args.data)
    X, y = split_features_target(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Compensate for the very small number of fraud examples.
    negatives = int((y_train == 0).sum())
    positives = int((y_train == 1).sum())
    ratio = negatives / max(positives, 1)

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=ratio,
        objective="binary:logistic",
        eval_metric="aucpr",
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_train, y_train)

    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "pr_auc_average_precision": float(average_precision_score(y_test, probabilities)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, predictions).tolist(),
        "fraud_examples_train": positives,
        "scale_pos_weight": float(ratio),
    }

    output = Path(args.model_out)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "feature_names": list(X.columns)}, output)

    # Log the run locally in MLflow.
    mlflow.set_experiment("financial-fraud-detection")
    with mlflow.start_run():
        mlflow.log_params({
            "model": "XGBClassifier",
            "n_estimators": 300,
            "max_depth": 5,
            "scale_pos_weight": ratio,
            "threshold": 0.5,
        })
        mlflow.log_metrics({
            k: v for k, v in metrics.items()
            if isinstance(v, (int, float))
        })
        mlflow.log_artifact(str(output))

    metrics_path = ROOT / "models" / "metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2))
    print("\nEvaluation metrics")
    print(json.dumps(metrics, indent=2))
    print("\nClassification report")
    print(classification_report(y_test, predictions, zero_division=0))
    print(f"\nSaved model: {output}")
    print(f"Saved metrics: {metrics_path}")

if __name__ == "__main__":
    main()
