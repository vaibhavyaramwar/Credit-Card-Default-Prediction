from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",["train_file_path","test_file_path","is_imbalanced","imbalenced_ratio","imbalanced_threshold","is_ingested","message"])
DataValidationArtifact = namedtuple("DataValidationArtifact",["schema_file_path","report_file_path","report_page_file_path","is_validated","message"])
DataTransformationArtifact = namedtuple("DataTransformationArtifact",["transformed_train_dir","transformed_test_dir","preprocessed_object_file_name","is_transformed","message"])
ModelTrainerArtifact = namedtuple("ModelTrainerArtifact",["is_trained","message","trained_model_file_path","model_name", "model_object", "train_accuracy","test_accuracy",
                                                            "model_accuracy","tp_train","tn_train","fn_train","fp_train",
                                                            "tp_test","tn_test","fn_test","fp_test",
                                                            "recall_train","recall_test",
                                                            "precision_train","precision_test",
                                                            "f1_score_train","f1_score_test",
                                                            "roc_auc_score_train","roc_auc_score_test"])
ModelEvaluationArtifact = namedtuple("ModelEvaluationArtifact",["is_model_accepted","evaluated_model_path"])
ModelPusherArtifact = namedtuple("ModelPusherArtifact",["is_model_pusher","export_model_file_path"])
