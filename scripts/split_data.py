# Split the cleaned data by order date into a training set and a held-out test set.
# Orders on or after TEST_START (the final ~11 days) form the test set, so the model is
# evaluated on later orders than it was trained on. The EDA and model tuning use train.csv only.

import argparse
import sys
from pathlib import Path

from food_delivery_utils import PROCESSED_DATA_PATH, TEST_PATH, TEST_START, TRAIN_PATH, load_processed

parser = argparse.ArgumentParser(description='Split the cleaned food delivery data by date.')
parser.add_argument('--data', type=Path, default=PROCESSED_DATA_PATH, help='path to the cleaned CSV from clean_data.py')
parser.add_argument('--train-out', type=Path, default=TRAIN_PATH, help='where to write the training set')
parser.add_argument('--test-out', type=Path, default=TEST_PATH, help='where to write the test set')
args = parser.parse_args()

if len({args.data.resolve(), args.train_out.resolve(), args.test_out.resolve()}) < 3:
    parser.error('--data, --train-out and --test-out must be three different files')

df = load_processed(args.data)

# drop_duplicates in clean_data.py only removes identical rows; a repeated ID could leak into both sets
if not df['ID'].is_unique:
    sys.exit('Duplicate order IDs found; the same order could end up in both train and test.')

is_test = df['date'] >= TEST_START
for out, part in [(args.train_out, df[~is_test]), (args.test_out, df[is_test])]:
    out.parent.mkdir(parents=True, exist_ok=True)
    part.to_csv(out, index=False)
    print(f'Wrote {len(part)} rows ({part["date"].min().date()} to {part["date"].max().date()}) to {out}')
