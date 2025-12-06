"""
Simple helper to prepare files for Aparavi ingestion.
This script copies files into a staging folder and optionally normalizes text.
"""
import argparse
import os
import shutil


def prepare_staging(source_dir: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    for root, _, files in os.walk(source_dir):
        for f in files:
            src = os.path.join(root, f)
            dst = os.path.join(out_dir, f)
            shutil.copy2(src, dst)
    print(f"Staged files from {source_dir} → {out_dir}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Prepare files for Aparavi ingestion')
    parser.add_argument('--source', required=True, help='Source folder containing sample docs')
    parser.add_argument('--out', default='staging_for_aparavi', help='Output staging folder')
    args = parser.parse_args()
    prepare_staging(args.source, args.out)
