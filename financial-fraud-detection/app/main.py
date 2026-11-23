"""FastAPI service for fraud predictions."""
from pathlib import Path
from typing import Dict

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "fraud_model.joblib"

app = FastAPI(title="Financial Fraud Detection API", version="1.0")

class Transaction(BaseModel):
    features: Dict[str, float]

def get_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run: python -m src.train")
    return joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok", "model_available": MODEL_PATH.exists()}

@app.post("/predict")
def predict(transaction: Transaction):
    try:
        bundle = get_bundle()
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    expected = bundle["feature_names"]
    missing = [name for name in expected if name not in transaction.features]
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing features: {missing}")
    row = pd.DataFrame(
        [[transaction.features[name] for name in expected]],
        columns=expected
    )
    probability = float(bundle["model"].predict_proba(row)[0, 1])
    label = "Fraud" if probability >= 0.5 else "Genuine"
    return {
        "fraud_probability": probability,
        "risk_percent": round(probability * 100, 2),
        "prediction": label,
        "threshold": 0.5,
    }
