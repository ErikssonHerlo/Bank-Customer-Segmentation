from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "bank-additional-full.csv"
RANDOM_STATE = 42

TARGET_COLUMN = "y"
UNKNOWN_TOKEN = "unknown"
DURATION_COLUMN = "duration"

NUMERIC_PLOTS_FIGSIZE = (10, 4)
CATEGORY_PLOTS_FIGSIZE = (10, 5)
CORRELATION_FIGSIZE = (12, 8)
PCA_FIGSIZE = (9, 7)
CLUSTER_PLOTS_FIGSIZE = (10, 6)

K_RANGE = range(2, 9)
HIERARCHICAL_SAMPLE_SIZE = 3000
DENDROGRAM_SAMPLE_SIZE = 400
PCA_COMPONENTS_FOR_CLUSTERING = 10
TOP_CATEGORY_LEVELS = 10

MONTH_ORDER = ["mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
DAY_ORDER = ["mon", "tue", "wed", "thu", "fri"]
