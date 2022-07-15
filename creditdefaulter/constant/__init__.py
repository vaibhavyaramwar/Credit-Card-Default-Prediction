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