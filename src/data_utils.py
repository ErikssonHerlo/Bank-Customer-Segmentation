from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from src.config import DURATION_COLUMN, TARGET_COLUMN, UNKNOWN_TOKEN


def load_bank_data(csv_path: str | None = None) -> pd.DataFrame:
    if csv_path is None:
        raise ValueError("csv_path is required.")
    return pd.read_csv(csv_path, sep=";")


def get_variable_types(df: pd.DataFrame, target_column: str = TARGET_COLUMN) -> Tuple[List[str], List[str]]:
    categorical_columns = df.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if target_column in categorical_columns:
        categorical_columns.remove(target_column)
    if target_column in numeric_columns:
        numeric_columns.remove(target_column)

    return numeric_columns, categorical_columns


def profiling_report(df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame(
        {
            "dtype": df.dtypes.astype(str),
            "missing_values": df.isna().sum(),
            "missing_rate": df.isna().mean(),
            "unique_values": df.nunique(dropna=False),
        }
    )

    unknown_counts = []
    unknown_rates = []

    for column in df.columns:
        if df[column].dtype == "object":
            count_unknown = (df[column] == UNKNOWN_TOKEN).sum()
            unknown_counts.append(int(count_unknown))
            unknown_rates.append(float(count_unknown / len(df)))
        else:
            unknown_counts.append(0)
            unknown_rates.append(0.0)

    report["unknown_values"] = unknown_counts
    report["unknown_rate"] = unknown_rates
    return report.sort_values(by=["missing_values", "unknown_values"], ascending=False)


def summarize_numeric(df: pd.DataFrame, numeric_columns: List[str]) -> pd.DataFrame:
    return df[numeric_columns].describe().T


def summarize_categorical(df: pd.DataFrame, categorical_columns: List[str]) -> Dict[str, pd.DataFrame]:
    summaries: Dict[str, pd.DataFrame] = {}
    for column in categorical_columns:
        counts = df[column].value_counts(dropna=False).rename_axis(column).reset_index(name="count")
        counts["proportion"] = counts["count"] / counts["count"].sum()
        summaries[column] = counts
    return summaries


def add_unknown_flags(df: pd.DataFrame, categorical_columns: List[str]) -> pd.DataFrame:
    df_copy = df.copy()
    for column in categorical_columns:
        df_copy[f"{column}_is_unknown"] = (df_copy[column] == UNKNOWN_TOKEN).astype(int)
    return df_copy


def replace_unknown_label(df: pd.DataFrame, categorical_columns: List[str], replacement: str = "Missing_Unknown") -> pd.DataFrame:
    df_copy = df.copy()
    for column in categorical_columns:
        df_copy[column] = df_copy[column].replace(UNKNOWN_TOKEN, replacement)
    return df_copy


def build_clustering_dataset(
    df: pd.DataFrame,
    categorical_columns: List[str],
    exclude_duration: bool = True,
    target_column: str = TARGET_COLUMN,
) -> pd.DataFrame:
    df_model = df.copy()

    if exclude_duration and DURATION_COLUMN in df_model.columns:
        df_model = df_model.drop(columns=[DURATION_COLUMN])

    if target_column in df_model.columns:
        df_model = df_model.drop(columns=[target_column])

    df_model = replace_unknown_label(df_model, categorical_columns=categorical_columns)
    return df_model
