from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.config.configuration import ModelTrainerConfig
from creditdefaulter.entity.config_entity import ModelTrainerConfig
from creditdefaulter.entity.artifact_entity import * 
from creditdefaulter.entity.model_factory import ModelFactory,CreditDefaultEstimatorModel
from creditdefaulter.entity.model_entity import GridSearchBestModel
from creditdefaulter.entity.model_entity import MetricInfoArtifact
from creditdefaulter.util import util

from typing import List

import os,sys


class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            transformed_train_dir = self.data_transformation_artifact.transformed_train_dir
            transformed_test_dir = self.data_transformation_artifact.transformed_test_dir
            
            train_array = util.load_numpy_arr_data(file_path=transformed_train_dir)
            test_array = util.load_numpy_arr_data(file_path=transformed_test_dir)
            logging.info( train_array)

            X_train,y_train,X_test,y_test = train_array[:,:-1],train_array[:,-1],test_array[:,:-1],test_array[:,-1]

            model_config_file_path = self.model_trainer_config.model_config_dir_file_path

            model_factory = ModelFactory(model_config_path=model_config_file_path)

            base_accuracy = self.model_trainer_config.base_accuracy

            best_model = model_factory.get_best_model(X=X_train,y=y_train,best_accuracy=base_accuracy)

            grid_searched_best_model_list : List[GridSearchBestModel] = model_factory.grid_searched_best_model_list

            model_list = [model.best_model for model in grid_searched_best_model_list]

            metricInfoArtifact:MetricInfoArtifact = ModelFactory.evaluate_classification_model(model_list,X_train,y_train, X_test,y_test,base_accuracy)

            processed_obj = util.load_obj(self.data_transformation_artifact.preprocessed_object_file_name)
            model_obj = metricInfoArtifact.model_object

            trained_model_file_path = self.model_trainer_config.trained_model_dir_file_path

            creditDefaultEstimatorModel = CreditDefaultEstimatorModel(preprocessing_object = processed_obj, trained_model_object = model_obj)

            util.save_obj(file_path=trained_model_file_path,obj=creditDefaultEstimatorModel)

            modelTrainerArtifact = ModelTrainerArtifact(is_trained = True,
                                                            message = "Model Training Successful",
                                                            trained_model_file_path = trained_model_file_path,
                                                            model_name = metricInfoArtifact.model_name,
                                                            model_object = metricInfoArtifact.model_object,
                                                            train_accuracy = metricInfoArtifact.train_accuracy,
                                                            test_accuracy = metricInfoArtifact.test_accuracy,
                                                            model_accuracy = metricInfoArtifact.model_accuracy,
                                                            tp_train = metricInfoArtifact.tp_train,
                                                            tn_train = metricInfoArtifact.tn_train,
                                                            fn_train = metricInfoArtifact.fn_train,
                                                            fp_train = metricInfoArtifact.fp_train,
                                                            tp_test = metricInfoArtifact.tp_test,
                                                            tn_test = metricInfoArtifact.tn_test,
                                                            fn_test = metricInfoArtifact.fn_test,
                                                            fp_test = metricInfoArtifact.fp_test,
                                                            recall_train = metricInfoArtifact.recall_train,
                                                            recall_test = metricInfoArtifact.recall_test,
                                                            precision_train = metricInfoArtifact.precision_train,
                                                            precision_test = metricInfoArtifact.precision_test,
                                                            f1_score_train = metricInfoArtifact.f1_score_train,
                                                            f1_score_test = metricInfoArtifact.f1_score_test,
                                                            roc_auc_score_train = metricInfoArtifact.roc_auc_score_train,
                                                            roc_auc_score_test = metricInfoArtifact.roc_auc_score_test)

            logging.info(f"Model Trainer Artifact : {modelTrainerArtifact}")
            
            return modelTrainerArtifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    