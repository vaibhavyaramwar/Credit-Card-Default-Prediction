from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["artifact_dir_path","dataset_download_file_name","raw_data_dir","extracted_download_dir","ingested_train_dir","ingested_test_dir"])



TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["name","artifact_dir"])