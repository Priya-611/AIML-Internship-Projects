# AIML-02 — Medical Image Analysis Platform

**Current status:** project scaffold and NIH dataset verification utilities. Model training, Grad-CAM, segmentation, API, React, Orthanc, DVC and Docker are future milestones and are not claimed as completed.

> **For educational and research purposes only. Not for clinical use.** This is not a medical device and must not be used to diagnose, treat, or guide patient care.

## Goal

Build an educational medical-image workflow that classifies chest X-ray images, generates Grad-CAM visualizations, and provides a radiologist-style review interface. Later stages add segmentation, DICOM ingestion, audit logging and containerization.

## Dataset

Selected dataset: **NIH ChestX-ray14**.

- Official page: https://nihcc.app.box.com/v/ChestXray-Nihcc
- 112,120 frontal-view chest X-ray images from 30,805 patients.
- 14 finding labels; this is a multi-label classification task.
- Metadata CSV commonly named `Data_Entry_2017_v2020.csv` (some copies use `Data_Entry_2017.csv`).
- Images are supplied as PNG files in image archives.

Download the metadata CSV and at least one image archive for initial development. The full dataset is large; start small and scale later. Follow the official dataset terms.

### Expected local layout

```text
dataset/
├── Data_Entry_2017_v2020.csv
└── images_001/
    ├── 00000001_000.png
    └── ...
```

The CSV describes the full dataset, while your local image folder may contain only a subset. The checker matches filenames. Do not commit dataset files to GitHub; `.gitignore` excludes them.

## Technologies

Python, PyTorch/Torchvision (DenseNet121), Grad-CAM, MONAI, FastAPI, React, Orthanc, DVC and Docker.

## Setup — Windows PowerShell

Create and activate an environment:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

If activation is blocked in the current PowerShell session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

Install PyTorch and Torchvision separately using the official selector for your hardware:

https://pytorch.org/get-started/locally/

Then install the remaining dependencies:

```powershell
pip install -r requirements.txt
```

Place the metadata CSV directly in `dataset/`, extract an image archive so PNGs are in `dataset/images_001/`, then run:

```powershell
python -m src.check_dataset
```

Optional: inspect an image:

```powershell
python -m src.inspect_image dataset/images_001/00000001_000.png
```

Run the starter tests:

```powershell
pip install pytest
pytest -q
```

## Folder structure

```text
AIML-02-Medical-Image-Analysis/
├── dataset/       # local dataset, excluded from Git
├── models/        # generated model files, excluded from Git
├── outputs/       # generated outputs, excluded from Git
├── src/
│   ├── check_dataset.py
│   └── inspect_image.py
├── backend/
├── frontend/
├── orthanc/
├── tests/
├── screenshots/
├── requirements.txt
└── README.md
```

## Planned milestones

1. Dataset download and inspection.
2. Image resize, normalization, augmentation and patient-level data split.
3. DenseNet121 multi-label classifier.
4. Per-label evaluation and Grad-CAM visualizations.
5. MONAI segmentation using a separate Medical Segmentation Decathlon dataset with segmentation masks.
6. FastAPI inference service.
7. React scan viewer with prediction, heatmap overlay, approve/reject controls and audit log.
8. Orthanc DICOM integration.
9. DVC data versioning and Docker packaging.

## Limitations and technical notes

- NIH ChestX-ray14 is multi-label: an image can have multiple findings; it is not just normal/abnormal binary classification.
- NIH images are PNG, not DICOM. Orthanc integration requires a separate DICOM test study or suitable DICOM dataset.
- NIH classification labels are not pixel-level segmentation masks. Segmentation needs a separate labeled dataset such as Medical Segmentation Decathlon.
- Grad-CAM highlights regions associated with model activations; it does not prove a disease is present.
- Performance may be affected by class imbalance, label noise, dataset composition, and demographic or acquisition biases. Dataset performance does not establish clinical safety.

## Screenshots and evidence

Store genuine screenshots in `screenshots/`: dataset verification, training metrics, Grad-CAM examples, API docs, React review page, and Orthanc/Docker once implemented. Only document features that have actually been implemented and tested.
