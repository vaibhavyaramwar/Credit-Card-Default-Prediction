from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["artifact_dir_path","dataset_download_file_name","raw_data_dir","extracted_download_dir","ingested_train_dir","ingested_test_dir"])
DataValidationConfig = namedtuple("DataValidationConfig",["artifact_dir_path","schema_dir","schema_file_path","report_file_name_path","report_page_file_path_name"])
DataTransformationConfig = namedtuple("DataTransformationConfig",["artifact_dir_path","transformed_train_dir","transformed_test_dir","preprocessed_object_file_name"])
ModelTrainerConfig = namedtuple("ModelTrainerConfig",["artifact_dir_path","trained_model_dir_file_path","base_accuracy","model_config_dir_file_path"])
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",["model_evaluation_file_name_path","time_stamp"])
ModelPusherConfig = namedtuple("ModelPusherConfig",["export_dir_path"])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig",["name","artifact_dir"])