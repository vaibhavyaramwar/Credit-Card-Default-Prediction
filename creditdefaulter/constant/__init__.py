import os
from datetime import datetime

ROOT_DIR = os.getcwd()
CONFIG_DIR = "config"
CONFIG_FILE = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

# Kaggle Variables

KAGGLE_USERNAME = "KAGGLE_USERNAME"
KAGGLE_KEY = "KAGGLE_KEY"
KAGGLE_USERNAME_VALUE = "vaibhavyaramwar"
KAGGLE_KEY_VALUE = "d06d519f9650b21805c3e7b5c33e63c9"

# Training Pipeline Variables

TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"


# Data Ingestion Variables

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_FILE_NAME_KEY = "dataset_download_file_name"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_EXTRACTED_DOWNLOAD_DIR_KEY = "extracted_download_dir"
DATA_INGESTION_INGESTED_DIR_KEY = "ingested_dir"
DATA_INGESTION_INGESTED_DIR_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_INGESTED_DIR_TEST_DIR_KEY = "ingested_test_dir"

# TARGET_COLUMN_NAME

TARGET_COLUMN_NAME = "default.payment.next.month"


# IMBALANCED THRESHOLD

IMBALANCED_THRESHOLD = 0.2


# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_ARTIFACT_DIR_NAME = "data_validation"
DATA_VALIDATION_REPORT_FILE_NAME_KEY = "report_file_name"
DATA_VALIDATION_REPORT_FILE_PATH_NAME_KEY = "report_page_file_path_name"
DATA_VALIDATION_DATA_DRIFT_KEY = "data_drift"
DATA_VALIDATION_DATA_DRIFT_DATA_KEY = "data"
DATA_VALIDATION_DATA_DRIFT_DATA_METRICS_KEY = "metrics"
DATA_VALIDATION_DATA_DRIFT_DATA_METRICS_DATASETDRIFT_KEY = "dataset_drift"



# TOTAL_COLUMNS

TOTAL_COLUMNS = 24

COLUMNS_ORDER_KEY = 'columns_order'
DOMAIN_VALUE_KEY = 'domain_value'
CATEGORICAL_COLUMNS_KEY = 'categorical_columns'