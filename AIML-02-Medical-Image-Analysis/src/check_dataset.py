"""Verify NIH ChestX-ray14 metadata and extracted PNG files."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset"
CSV_CANDIDATES = [
    DATA / "Data_Entry_2017_v2020.csv",
    DATA / "Data_Entry_2017.csv",
]
REQUIRED = {"Image Index", "Finding Labels"}

def main():
    csv_path = next((p for p in CSV_CANDIDATES if p.is_file()), None)
    if csv_path is None:
        print("Metadata CSV not found. Place Data_Entry_2017_v2020.csv (or Data_Entry_2017.csv) in:")
        print(DATA)
        return 1

    df = pd.read_csv(csv_path)
    missing = REQUIRED - set(df.columns)
    if missing:
        print(f"Missing required metadata columns: {sorted(missing)}")
        return 1

    folders = [p for p in DATA.glob("images*") if p.is_dir()]
    images = [img for folder in folders for img in folder.glob("*.png")]
    metadata_names = set(df["Image Index"].astype(str))
    matching = sum(img.name in metadata_names for img in images)

    print(f"Metadata file: {csv_path.name}")
    print(f"Metadata rows: {len(df):,}")
    print(f"Unique metadata image names: {df['Image Index'].nunique():,}")
    print(f"Image folders: {len(folders)}")
    print(f"PNG files found: {len(images):,}")
    print(f"Image filenames matching metadata: {matching:,}")
    print("\nMost common label combinations:")
    print(df["Finding Labels"].value_counts().head(10).to_string())

    if not images:
        print("\nNo PNG images found. Extract at least one NIH image archive into dataset/.")
        return 2
    if matching == 0:
        print("\nNo image filenames matched the CSV. Check the extraction folder layout.")
        return 2

    print("\nDataset check passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
