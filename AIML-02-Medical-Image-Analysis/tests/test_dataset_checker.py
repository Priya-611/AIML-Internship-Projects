from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.check_dataset import REQUIRED, CSV_CANDIDATES

def test_required_columns():
    assert REQUIRED == {"Image Index", "Finding Labels"}

def test_csv_candidates_are_in_dataset_folder():
    assert all(p.parent.name == "dataset" for p in CSV_CANDIDATES)
