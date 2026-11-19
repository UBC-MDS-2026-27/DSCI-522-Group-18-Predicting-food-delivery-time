# # Clean the raw Food Delivery Dataset and write the processed file used by the EDA and modeling.
# Fixes: duplicate rows, trailing spaces in names/values, 'NaN ' strings, text-typed numerics, the 'conditions '
# weather prefix and the '(min) ' target prefix; adds parsed date/time, distance and courier city.
# Rows without an order date or a delivery time are dropped: they can't be split by date or used as labels.
# The 91 corrupted rows (impossible ages/ratings) are kept so the EDA can show them;
# the modeling script removes them with `drop_corrupted`.

import argparse
import sys
from pathlib import Path

from food_delivery_utils import PROCESSED_COLS, PROCESSED_DATA_PATH, RAW_DATA_PATH, load_clean

parser = argparse.ArgumentParser(description='Clean the raw food delivery data.')
parser.add_argument('--raw', type=Path, default=RAW_DATA_PATH, help='path to the raw train.csv')
parser.add_argument('--out', type=Path, default=PROCESSED_DATA_PATH, help='where to write the cleaned CSV')
args = parser.parse_args()

if args.raw.resolve() == args.out.resolve():
    parser.error('--out must be a different file from --raw (it would overwrite the raw data)')

df = load_clean(args.raw)[PROCESSED_COLS]

n_before = len(df)
df = df.drop_duplicates()
print(f'Removed {n_before - len(df)} duplicate rows')

unusable = df['date'].isna() | df['target'].isna()
df = df[~unusable]
print(f'Removed {unusable.sum()} rows with a missing order date or delivery time')
if df.empty:
    sys.exit('No usable rows left (every row lacks an order date or delivery time); nothing was written.')

args.out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(args.out, index=False)
print(f'Wrote {len(df)} rows x {df.shape[1]} columns to {args.out}')
