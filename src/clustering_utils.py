from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_preprocessor(numeric_columns: List[str], categorical_columns: List[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_columns),
            ("categorical", categorical_pipeline, categorical_columns),
        ],
        remainder="drop",
    )


def transform_features(
    df: pd.DataFrame,
    numeric_columns: List[str],
    categorical_columns: List[str],
) -> Tuple[np.ndarray, ColumnTransformer, List[str]]:
    preprocessor = build_preprocessor(numeric_columns=numeric_columns, categorical_columns=categorical_columns)
    transformed = preprocessor.fit_transform(df)

    feature_names = []
    feature_names.extend(numeric_columns)

    encoder = preprocessor.named_transformers_["categorical"].named_steps["encoder"]
    categorical_feature_names = encoder.get_feature_names_out(categorical_columns).tolist()
    feature_names.extend(categorical_feature_names)

    return transformed, preprocessor, feature_names


def evaluate_kmeans_range(features: np.ndarray, k_values: Iterable[int], random_state: int = 42) -> pd.DataFrame:
    rows = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=random_state, n_init=20)
        labels = model.fit_predict(features)
        silhouette = silhouette_score(features, labels, sample_size=min(10000, len(features)), random_state=random_state)
        rows.append({"k": k, "inertia": float(model.inertia_), "silhouette_score": float(silhouette)})
    return pd.DataFrame(rows)


def select_best_k(results: pd.DataFrame) -> int:
    return int(results.sort_values(by=["silhouette_score", "k"], ascending=[False, True]).iloc[0]["k"])


def fit_kmeans(features: np.ndarray, n_clusters: int, random_state: int = 42) -> Tuple[KMeans, np.ndarray]:
    model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=20)
    labels = model.fit_predict(features)
    return model, labels


def fit_pca(features: np.ndarray, n_components: int = 10) -> Tuple[PCA, np.ndarray]:
    pca = PCA(n_components=n_components, random_state=42)
    transformed = pca.fit_transform(features)
    return pca, transformed


def fit_hierarchical(features: np.ndarray, n_clusters: int, linkage_method: str = "ward") -> Tuple[AgglomerativeClustering, np.ndarray]:
    model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage_method)
    labels = model.fit_predict(features)
    return model, labels


def hierarchical_linkage_matrix(features: np.ndarray, method: str = "ward") -> np.ndarray:
    return linkage(features, method=method)


def cluster_profile(
    df_original: pd.DataFrame,
    labels: np.ndarray,
    numeric_columns: List[str],
    categorical_columns: List[str],
    target_column: str = "y",
    positive_label: str = "yes",
) -> Dict[str, pd.DataFrame]:
    profiled_df = df_original.copy()
    profiled_df["cluster"] = labels

    size_table = profiled_df["cluster"].value_counts().sort_index().rename("records").reset_index()
    size_table.columns = ["cluster", "records"]
    size_table["share"] = size_table["records"] / len(profiled_df)

    numeric_profile = profiled_df.groupby("cluster")[numeric_columns].mean().round(3)

    target_profile = (
        profiled_df.groupby("cluster")[target_column]
        .agg(total="count", conversions=lambda series: (series == positive_label).sum())
        .assign(conversion_rate=lambda frame: frame["conversions"] / frame["total"])
        .round(4)
    )

    categorical_mode_rows = []
    for cluster_value, cluster_frame in profiled_df.groupby("cluster"):
        row = {"cluster": cluster_value}
        for column in categorical_columns:
            row[f"{column}_mode"] = cluster_frame[column].mode(dropna=False).iloc[0]
        categorical_mode_rows.append(row)
    categorical_profile = pd.DataFrame(categorical_mode_rows).set_index("cluster")

    return {
        "size_table": size_table,
        "numeric_profile": numeric_profile,
        "target_profile": target_profile,
        "categorical_profile": categorical_profile,
        "profiled_df": profiled_df,
    }


def business_segment_name(target_profile: pd.DataFrame) -> pd.DataFrame:
    result = target_profile.copy()
    names = []
    for conversion_rate in result["conversion_rate"]:
        if conversion_rate >= 0.50:
            names.append("High Conversion Potential")
        elif conversion_rate >= 0.25:
            names.append("Responsive Growth Segment")
        elif conversion_rate >= 0.10:
            names.append("Selective Opportunity Segment")
        else:
            names.append("Low Response Efficiency Segment")
    result["strategic_name"] = names
    return result
