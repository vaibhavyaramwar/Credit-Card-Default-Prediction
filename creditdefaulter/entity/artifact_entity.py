from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path","is_imbalanced","imbalenced_ratio","imbalanced_threshold","is_ingested","message"])
DataValidationArtifact = namedtuple("DataValidationArtifact",["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])
DataTransformationArtifact = namedtuple("DataTransformationArtifact",["transformed_train_dir","transformed_test_dir","preprocessed_object_file_name","is_transformed","message"])