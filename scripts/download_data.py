# # Download the Food Delivery Dataset (Gaurav Malik) from Kaggle into data/raw/.
# Uses Kaggle's official `kagglehub` client. The dataset is public, so no Kaggle account or
# API token is needed. Version 1 is pinned so everyone gets exactly the same files.

import argparse
import shutil
import sys
from pathlib import Path

import kagglehub

from food_delivery_utils import RAW_DATA_PATH

DATASET = 'gauravmalik26/food-delivery-dataset/versions/1'
EXPECTED_FILES = ['train.csv', 'test.csv', 'Sample_Submission.csv']

parser = argparse.ArgumentParser(description='Download the raw food delivery data from Kaggle.')
parser.add_argument('--out-dir', type=Path, default=RAW_DATA_PATH.parent,
                    help='folder to copy the downloaded files into')
args = parser.parse_args()

cache_dir = Path(kagglehub.dataset_download(DATASET))

# Check every file first, so an incomplete download never mixes new and stale files in out-dir
missing = [name for name in EXPECTED_FILES if not (cache_dir / name).is_file()]
if missing:
    sys.exit(f'Download incomplete: {", ".join(missing)} not found in {cache_dir}. '
             'Delete that folder and run this script again.')

args.out_dir.mkdir(parents=True, exist_ok=True)
for name in EXPECTED_FILES:
    shutil.copy2(cache_dir / name, args.out_dir / name)
    print(f'Wrote {args.out_dir / name}')
