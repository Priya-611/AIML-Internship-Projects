"""Streamlit analyst dashboard. Start the FastAPI service first."""
from pathlib import Path
import requests
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "dataset" / "creditcard.csv"

st.set_page_config(page_title="Fraud Detection", page_icon="🛡️", layout="wide")
st.title("🛡️ Financial Fraud Detection")
st.caption("Simple analyst dashboard — predictions are made by the FastAPI model service.")

api_url = st.sidebar.text_input("Prediction API URL", "http://127.0.0.1:8000")
uploaded = st.sidebar.file_uploader("Upload creditcard.csv (optional)", type=["csv"])

@st.cache_data
def read_csv_file(file_bytes=None):
    if file_bytes is not None:
        import io
        return pd.read_csv(io.BytesIO(file_bytes))
    return pd.read_csv(DEFAULT_DATA)

try:
    if uploaded is not None:
        data = read_csv_file(uploaded.getvalue())
    elif DEFAULT_DATA.exists():
        data = read_csv_file()
    else:
        st.info("Put creditcard.csv in the dataset folder, or upload it using the sidebar.")
        st.stop()
except Exception as exc:
    st.error(f"Could not read dataset: {exc}")
    st.stop()

if "cases" not in st.session_state:
    st.session_state.cases = []

st.subheader("Transaction replay")
st.write("Choose a transaction from the dataset and send its features to the prediction API.")
max_index = min(len(data) - 1, 10000)
index = st.number_input("Transaction row", min_value=0, max_value=max_index, value=0, step=1)
row = data.iloc[int(index)]
features = row.drop(labels=["Class"], errors="ignore").to_dict()

col1, col2 = st.columns([1, 2])
with col1:
    st.metric("Transaction amount", f"${float(row.get('Amount', 0)):.2f}")
    if "Class" in row:
        st.caption("Dataset label (for demo/evaluation only): " + ("Fraud" if int(row["Class"]) == 1 else "Genuine"))
with col2:
    if st.button("Score transaction", type="primary"):
        try:
            response = requests.post(
                f"{api_url.rstrip('/')}/predict",
                json={"features": {k: float(v) for k, v in features.items()}},
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()
            case = {
                "row": int(index),
                "amount": float(row.get("Amount", 0)),
                "prediction": result["prediction"],
                "risk": result["risk_percent"],
                "status": "Open",
                "analyst_label": "Not reviewed",
            }
            st.session_state.cases.insert(0, case)
            st.success(f"{result['prediction']} — fraud risk {result['risk_percent']}%")
        except requests.RequestException as exc:
            st.error(f"Could not reach prediction API. Start it first. Details: {exc}")

st.divider()
st.subheader("Analyst case queue")
if st.session_state.cases:
    cases_df = pd.DataFrame(st.session_state.cases)
    st.dataframe(cases_df, use_container_width=True, hide_index=True)
    selected = st.selectbox("Select case row to review", options=list(range(len(st.session_state.cases))))
    label_col, status_col = st.columns(2)
    with label_col:
        analyst_label = st.selectbox("Feedback label", ["Not reviewed", "Fraud", "Genuine"], key="feedback")
    with status_col:
        status = st.selectbox("Case status", ["Open", "Investigating", "Closed"], key="case_status")
    if st.button("Save analyst review"):
        st.session_state.cases[selected]["analyst_label"] = analyst_label
        st.session_state.cases[selected]["status"] = status
        st.success("Review saved for this dashboard session.")
else:
    st.info("No scored transactions yet. Score a transaction above to create a case.")

st.divider()
st.subheader("Dataset overview")
if "Class" in data:
    counts = data["Class"].value_counts().rename(index={0: "Genuine", 1: "Fraud"})
    c1, c2, c3 = st.columns(3)
    c1.metric("Total transactions", f"{len(data):,}")
    c2.metric("Genuine", f"{int((data['Class'] == 0).sum()):,}")
    c3.metric("Fraud", f"{int((data['Class'] == 1).sum()):,}")
    st.bar_chart(counts)
