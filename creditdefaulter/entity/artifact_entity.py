from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path","is_imbalanced","imbalenced_ratio","imbalanced_threshold","is_ingested","message"])
