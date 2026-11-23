"""Print basic properties of a local NIH PNG image."""
import argparse
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Path to a PNG image")
    path = Path(parser.parse_args().image)
    if not path.is_file():
        raise SystemExit(f"Image not found: {path}")
    with Image.open(path) as img:
        print(f"File: {path}")
        print(f"Format: {img.format}")
        print(f"Mode: {img.mode}")
        print(f"Dimensions: {img.width} x {img.height}")

if __name__ == "__main__":
    main()
