# clustering/preprocess.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from typing import List, Tuple, Optional


def preprocess_data_clustering(features_by_patient):

    features_by_patient = pd.DataFrame.from_dict(features_by_patient, orient='index')

    features_by_patient = features_by_patient.apply(pd.to_numeric, errors='ignore')

    one_hot_features = _apply_onehot(features_by_patient)
    normalized_features,_ = _apply_normalization(one_hot_features)

    normalized_features = normalized_features.rename(str,axis="columns") 

    return normalized_features

def _apply_onehot(features_by_patient):
    non_numeric_cols = features_by_patient.select_dtypes(exclude=['number']).columns
    return pd.get_dummies(features_by_patient, columns=non_numeric_cols)


def _apply_normalization(df: pd.DataFrame):
    numeric_cols, _ = get_numeric_and_non_numeric_cols(df)
    out = df.copy()

    if not numeric_cols:
        # Nothing to do
        return out, numeric_cols

    scaler = StandardScaler() # z-score normalization
    out[numeric_cols] = scaler.fit_transform(out[numeric_cols])

    return out, numeric_cols



def get_numeric_and_non_numeric_cols(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Return lists of numeric and non-numeric column names."""
    numeric = df.select_dtypes(include="number").columns.tolist()
    non_numeric = [c for c in df.columns if c not in numeric]
    return numeric, non_numeric