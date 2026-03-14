from __future__ import annotations

from typing import Iterable, List

import numpy as np
import pandas as pd
from scipy.stats import zscore


def iqr_outlier_summary(df: pd.DataFrame, numeric_columns: Iterable[str]) -> pd.DataFrame:
    rows = []
    for column in numeric_columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = ((df[column] < lower_bound) | (df[column] > upper_bound)).sum()
        rows.append(
            {
                "variable": column,
                "q1": q1,
                "q3": q3,
                "iqr": iqr,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": int(outliers),
                "outlier_rate": float(outliers / len(df)),
            }
        )
    return pd.DataFrame(rows).sort_values(by="outlier_rate", ascending=False)


def zscore_outlier_summary(df: pd.DataFrame, numeric_columns: Iterable[str], threshold: float = 3.0) -> pd.DataFrame:
    rows = []
    for column in numeric_columns:
        scores = np.abs(zscore(df[column], nan_policy="omit"))
        outliers = np.sum(scores > threshold)
        rows.append(
            {
                "variable": column,
                "z_threshold": threshold,
                "outlier_count": int(outliers),
                "outlier_rate": float(outliers / len(df)),
            }
        )
    return pd.DataFrame(rows).sort_values(by="outlier_rate", ascending=False)


def conversion_rate_by_category(
    df: pd.DataFrame,
    categorical_column: str,
    target_column: str = "y",
    positive_label: str = "yes",
) -> pd.DataFrame:
    summary = (
        df.groupby(categorical_column)[target_column]
        .agg(records="count", conversions=lambda series: (series == positive_label).sum())
        .reset_index()
    )
    summary["conversion_rate"] = summary["conversions"] / summary["records"]
    return summary.sort_values(by=["conversion_rate", "records"], ascending=[False, False])


def numeric_summary_by_target(df: pd.DataFrame, numeric_columns: List[str], target_column: str = "y") -> pd.DataFrame:
    return df.groupby(target_column)[numeric_columns].mean().T


def redundancy_pairs(correlation_matrix: pd.DataFrame, threshold: float = 0.75) -> pd.DataFrame:
    rows = []
    columns = correlation_matrix.columns.tolist()
    for i, col_left in enumerate(columns):
        for j, col_right in enumerate(columns):
            if j <= i:
                continue
            correlation_value = correlation_matrix.loc[col_left, col_right]
            if abs(correlation_value) >= threshold:
                rows.append(
                    {
                        "variable_1": col_left,
                        "variable_2": col_right,
                        "correlation": correlation_value,
                    }
                )
    if not rows:
        return pd.DataFrame(columns=["variable_1", "variable_2", "correlation"])
    return pd.DataFrame(rows).sort_values(by="correlation", ascending=False)
