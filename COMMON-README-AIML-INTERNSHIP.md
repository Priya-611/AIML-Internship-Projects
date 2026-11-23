# AIML Internship Projects

This public repository contains two separate AI/ML internship projects. Each project has its own source code, dependencies, setup instructions and README.

## AIML-01 — Real-Time Financial Fraud Detection

An educational transaction-fraud prototype using a credit-card transaction dataset, XGBoost, MLflow, FastAPI and Streamlit.

**Current implementation:** XGBoost training with imbalance-aware evaluation, MLflow experiment tracking, FastAPI prediction endpoint, Streamlit dashboard, and CSV-based transaction replay simulation.

**Further milestones:** Kafka streaming, graph-based fraud-ring analysis, Feast feature store, Evidently drift monitoring and Kubernetes deployment. These should be marked complete only after implementation and testing.

Project folder: [`AIML-01-Fraud-Detection/`](AIML-01-Fraud-Detection/)

## AIML-02 — Medical Image Analysis Platform

An educational medical-image project selected to use NIH ChestX-ray14 for multi-label chest X-ray classification, with planned Grad-CAM explanations, MONAI segmentation, FastAPI, React, Orthanc DICOM integration, DVC and Docker.

**Current implementation:** project scaffold and NIH dataset verification scripts.

**Further milestones:** DenseNet121 training, Grad-CAM, segmentation, inference API, React review interface and audit log, Orthanc, DVC and Docker. These are not claimed as completed until implemented and tested.

Project folder: [`AIML-02-Medical-Image-Analysis/`](AIML-02-Medical-Image-Analysis/)

## Repository structure

```text
AIML-Internship-Projects/
├── AIML-01-Fraud-Detection/
├── AIML-02-Medical-Image-Analysis/
└── README.md
```

## Setup

Each project has its own dependencies and setup instructions. Open the relevant project folder and follow its README.

## Data, models and security

- Do not commit large datasets, virtual environments, model binaries, API keys, credentials or patient-identifying information.
- Follow each dataset's terms of use.
- Keep screenshots free of private information.
- Use Git LFS or an approved artifact store only when necessary and permitted.

## Suggested commit history

Use small, descriptive commits, for example:

```text
Add AIML-02 project scaffold
Add NIH dataset verification utility
Implement image preprocessing
Train DenseNet121 multi-label classifier
Add Grad-CAM visualization
Add FastAPI inference endpoint
Build React review dashboard
Add Orthanc Docker configuration
```

## Safety and intended use

Both projects are educational prototypes, not production systems.

- **AIML-01:** experimental fraud predictions should not be the sole basis for financial decisions.
- **AIML-02:** for educational and research purposes only; not for clinical use. It is not a medical device and must not be used to diagnose, treat, or guide patient care.

## Submission checklist

- [ ] Set repository visibility to Public if required by the evaluation team.
- [ ] Keep the two projects in separate folders.
- [ ] Include project-specific READMEs, source code and tests.
- [ ] Add genuine screenshots of working features.
- [ ] Document architecture, setup, execution, metrics, limitations and next steps.
- [ ] Exclude datasets, secrets, virtual environments and large generated artifacts.
- [ ] Maintain meaningful Git commits.
