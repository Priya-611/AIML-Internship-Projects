"""Helpers for preparing the ULB credit-card fraud dataset."""
import pandas as pd

TARGET = "Class"

def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if TARGET not in df.columns:
        raise ValueError("Dataset must contain a 'Class' target column.")
    return df

def split_features_target(df: pd.DataFrame):
    X = df.drop(columns=[TARGET])
    y = df[TARGET].astype(int)
    return X, y
