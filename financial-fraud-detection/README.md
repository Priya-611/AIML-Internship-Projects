# Real-Time Financial Fraud Detection (Simple MVP)

A beginner-friendly version of the assigned project. It trains an XGBoost model, serves predictions through FastAPI, and provides an analyst dashboard using Streamlit.

## What is included

- Credit-card fraud dataset loading and basic preprocessing
- Imbalance-aware XGBoost training (`scale_pos_weight`)
- Evaluation using PR-AUC / average precision, precision, recall and F1
- MLflow experiment tracking
- FastAPI `/predict` endpoint
- Streamlit dashboard with transaction scoring, case status and analyst feedback
- Manual transaction replay from the CSV for a simple real-time-style demo

## 1. Get the dataset

Download `creditcard.csv` from:
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

Place it here:

`dataset/creditcard.csv`

The CSV should contain columns `Time`, `V1` ... `V28`, `Amount`, and `Class`.

## 2. Create an environment (Windows PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Train the model

Run from the project root:

```powershell
python -m src.train
```

This creates:
- `models/fraud_model.joblib`
- `models/metrics.json`
- `mlruns/` (MLflow tracking data)

The test split is stratified so the small fraud class is represented in both training and test sets. Do not use accuracy as the main metric because the dataset is highly imbalanced.

To view MLflow runs:

```powershell
mlflow ui
```

Open the local address printed by MLflow (usually http://127.0.0.1:5000).

## 4. Start the API

Open a **second terminal**, activate the same environment, and run:

```powershell
uvicorn app.main:app --reload
```

Check:
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## 5. Start the dashboard

Open a **third terminal**, activate the environment, and run:

```powershell
streamlit run app/dashboard.py
```

Choose a transaction row and click **Score transaction**. The dashboard sends its features to FastAPI and displays the model's prediction. Analyst feedback is kept in the current Streamlit session.

## Important project scope

This is the simple working MVP, not every advanced item in the assignment. The CSV replay simulates incoming transactions; it is not Kafka. The current MVP does not yet include Feast, graph neural networks/fraud rings, Evidently drift-trigger automation, or Kubernetes. Add those only after this core pipeline works. For a graph extension, use account/device identifiers from a suitable dataset; the ULB credit-card CSV does not contain those relationship fields.

## Suggested demo

1. Show the dataset class imbalance.
2. Run training and show PR-AUC, precision and recall.
3. Open MLflow and show the recorded experiment.
4. Open FastAPI docs and call `/predict`.
5. Replay a few transactions in Streamlit.
6. Show the case queue and analyst feedback.

## Folder structure

```text
financial-fraud-detection/
├── dataset/
├── models/
├── src/
│   ├── preprocessing.py
│   └── train.py
├── app/
│   ├── main.py
│   └── dashboard.py
├── requirements.txt
└── README.md
```
