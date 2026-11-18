# Shared loading and cleaning for the Food Delivery Time dataset (Kaggle, Gaurav Malik).
# Used by eda_food_delivery.py and modeling_food_delivery.py so both see identical data.

import os
import shutil
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = ROOT / 'data' / 'raw' / 'Food_Delivery_Dataset' / 'train.csv'
PROCESSED_DATA_PATH = ROOT / 'data' / 'processed' / 'food_delivery_clean.csv'
TRAIN_PATH = ROOT / 'data' / 'processed' / 'train.csv'
TEST_PATH = ROOT / 'data' / 'processed' / 'test.csv'

# Orders on or after this date form the held-out test set (the final ~11 days)
TEST_START = pd.Timestamp('2022-03-27')

COORD_COLS = ['Restaurant_latitude', 'Restaurant_longitude',
              'Delivery_location_latitude', 'Delivery_location_longitude']
LAT_COLS = ['Restaurant_latitude', 'Delivery_location_latitude']
LON_COLS = ['Restaurant_longitude', 'Delivery_location_longitude']

# Columns written to the processed file (raw text columns are replaced by their parsed versions)
PROCESSED_COLS = (['ID', 'Delivery_person_ID', 'courier_city', 'Age', 'Rating', 'Vehicle_condition',
                   'Type_of_vehicle', 'multiple_deliveries', 'Weatherconditions', 'Road_traffic_density',
                   'Type_of_order', 'Festival', 'City', 'date', 'dow', 'order_hour', 'prep_min']
                  + COORD_COLS + ['dist_km', 'target'])

# Impossible values that only occur in the 91 corrupted rows found in the EDA
BAD_AGES = [15, 50]
BAD_RATINGS = [1, 6]


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance in km."""
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    a = (np.sin((lat2 - lat1) / 2) ** 2
         + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2)
    return 6371 * 2 * np.arcsin(np.sqrt(a))


def coords_valid(df):
    """True where all coordinates are finite, within lat/lon bounds and not placeholders (|x| < 1)."""
    coords = df[COORD_COLS].abs()
    return (np.isfinite(coords).all(axis=1)
            & (coords >= 1).all(axis=1)
            & (coords[LAT_COLS] <= 90).all(axis=1)
            & (coords[LON_COLS] <= 180).all(axis=1))


def distance_km(df):
    """Distance on absolute coordinates (fixes sign errors); NaN where any coordinate is invalid."""
    coords = df[COORD_COLS].abs().where(coords_valid(df), axis=0)
    return haversine_km(*(coords[c] for c in COORD_COLS))


def load_clean(path=RAW_DATA_PATH):
    """Read the raw CSV, normalise strings/missing values, parse types and derive base columns."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    for c in df.select_dtypes(exclude='number').columns:
        df[c] = df[c].astype(str).str.strip().replace({'NaN': np.nan, 'nan': np.nan})

    # 'conditions Sunny' -> 'Sunny', 'conditions NaN' -> NaN
    df['Weatherconditions'] = (df['Weatherconditions']
                               .str.replace('conditions ', '', regex=False)
                               .replace('NaN', np.nan))

    if 'Time_taken(min)' in df:
        # astype('string') so this also works when pandas reads an all-blank column as numeric
        df['target'] = pd.to_numeric(df['Time_taken(min)'].astype('string')
                                     .str.replace('(min) ', '', regex=False)).astype(float)

    df['Age'] = pd.to_numeric(df['Delivery_person_Age'])
    df['Rating'] = pd.to_numeric(df['Delivery_person_Ratings'])
    df['multiple_deliveries'] = pd.to_numeric(df['multiple_deliveries'])

    df['date'] = pd.to_datetime(df['Order_Date'], format='%d-%m-%Y')
    df['dow'] = df['date'].dt.dayofweek

    ordered = pd.to_datetime(df['Time_Orderd'], format='%H:%M:%S', errors='coerce')
    picked = pd.to_datetime(df['Time_Order_picked'], format='%H:%M:%S', errors='coerce')
    df['order_hour'] = ordered.dt.hour
    prep = (picked - ordered).dt.total_seconds() / 60
    df['prep_min'] = prep.where(prep >= 0, prep + 24 * 60)  # pickup after midnight

    df['courier_city'] = df['Delivery_person_ID'].str.extract(r'^([A-Z]+?)RES')[0]
    df['dist_km'] = distance_km(df)
    return df


def load_processed(path=PROCESSED_DATA_PATH):
    """Read a cleaned file written by clean_data.py or split_data.py."""
    return pd.read_csv(path, parse_dates=['date'])


def drop_corrupted(df):
    """Remove the rows with impossible courier ages/ratings."""
    bad = df['Age'].isin(BAD_AGES) | df['Rating'].isin(BAD_RATINGS)
    return df[~bad].reset_index(drop=True)


def _temp_sibling(path):
    """Create an empty temporary file next to path. It ends with path's own suffixes
    (e.g. '.csv.gz') so pandas infers the same format and compression as for path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f'.{path.name}.',
                               suffix=f'.tmp{"".join(path.suffixes)}')
    os.close(fd)
    return Path(tmp)


def write_csv_atomic(df, path):
    """Write df to path as CSV without ever leaving a partial file at path."""
    path = Path(path)
    tmp = _temp_sibling(path)
    try:
        df.to_csv(tmp, index=False)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def copy_all_atomic(pairs):
    """Copy each (src, dst) pair. Every file is copied to a temporary sibling first, and
    destinations are replaced only once all copies have succeeded, so a failure part-way
    leaves every existing destination untouched."""
    pairs = [(Path(src), Path(dst)) for src, dst in pairs]
    blocked = [dst for _, dst in pairs if dst.is_dir()]
    if blocked:
        raise IsADirectoryError(f'Cannot replace {blocked[0]}: a directory is in the way')

    staged = []
    try:
        for src, dst in pairs:
            tmp = _temp_sibling(dst)
            staged.append((tmp, dst))
            shutil.copy2(src, tmp)
        for tmp, dst in staged:
            os.replace(tmp, dst)
    finally:
        for tmp, _ in staged:
            tmp.unlink(missing_ok=True)
