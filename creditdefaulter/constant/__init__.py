import os
from datetime import datetime

ROOT_DIR = os.getcwd()
CONFIG_DIR = "config"
CONFIG_FILE = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE)

CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"


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

HOUSING_DATA_KEY = "credit_card_data"
MEDIAN_HOUSING_VALUE_KEY = "default_payment_next_month"


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

TOTAL_COLUMNS = 25

COLUMNS_KEY = 'columns'
COLUMNS_ORDER_KEY = 'columns_order'
DOMAIN_VALUE_KEY = 'domain_value'
CATEGORICAL_COLUMNS_KEY = 'categorical_columns'
NUMERICAL_COLUMN_KEY = 'numerical_columns'


# DATA TRANSFORMATION

DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY = "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY = "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY = "preprocessed_object_file_name"

CATEGORICAL_COLUMN_THRESHOLD =  0.05

# MODEL TRAINING

MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
MODEL_TRAINER_CONFIG_KEY="model_trainer_config"
TRAINED_MODEL_DIR_KEY="trained_model_dir"
MODEL_FILE_NAME_KEY="model_File_name"
BASE_ACCURACY_KEY="base_accuracy"
MODEL_CONFIG_DIR_KEY="model_config_dir"
MODEL_CONFIG_FILE_NAME_KEY="model_config_file_name"


# MODEL Yaml CONSTANT

GRID_SEARCH_CONFIG_KEY = "grid_search"
GRID_SEARCH_CLASS_KEY = "class"
GRID_SEARCH_MODULE_KEY = "module"
GRID_SEARCH_PARAMS_KEY = "params"
MODEL_SELECTION_KEY = "model_selection"
MODEL_SELECTION_PARAMS_KEY = "params"
MODEL_SELECTION_SEARCH_PARAM_GRID_KEY = "search_param_grid"


# MODEL EVALUATION

MODEL_EVALUATION_ARTIFACT_DIR = "model_evaluation"
MODEL_EVALUATION_CONFIG_KEY = "model_evaluation_config"
MODEL_EVALUATION_FILE_NAME_KEY = "model_evaluation_file_name"

SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)



BEST_MODEL_KEY = "best_model"
HISTORY_KEY = "history"
MODEL_PATH_KEY = "model_path"


# MODEL PUSHER

MODEL_PUSHER_CONFIG_KEY = "model_pusher_config"
MODEL_PUSHER_EXPORT_DIR_KEY = "model_export_dir"



EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"


LOG_FOLDER_NAME = "logs"


MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")

