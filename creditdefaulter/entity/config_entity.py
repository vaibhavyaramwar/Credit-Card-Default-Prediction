from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["artifact_dir_path","dataset_download_file_name","raw_data_dir","extracted_download_dir","ingested_train_dir","ingested_test_dir"])
DataValidationConfig = namedtuple("DataValidationConfig",["artifact_dir_path","schema_dir","schema_file_path","report_file_name_path","report_page_file_path_name"])


TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["name","artifact_dir"])