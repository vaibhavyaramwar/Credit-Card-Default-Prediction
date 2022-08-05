
from collections import namedtuple


BestModel = namedtuple("BestModel",["model_serial_no","model","best_model","best_parameter","best_score"])
InitializedModelDetail = namedtuple("InitializedModelDetail",["model_serial_no","model","param_grid_Search","model_name"])
GridSearchBestModel = namedtuple("GridSearchBestModel",["model_serial_no","model","best_model","best_parameters","best_scores"])
MetricInfoArtifact = namedtuple("MetricInfoArtifact",["model_name", "model_object", "train_accuracy","test_accuracy", 
                                                        "model_accuracy","tp_train","tn_train","fn_train","fp_train",
                                                        "tp_test","tn_test","fn_test","fp_test",
                                                        "recall_train","recall_test",
                                                        "precision_train","precision_test",
                                                        "f1_score_train","f1_score_test",
                                                        "roc_auc_score_train","roc_auc_score_test","index_number"])

