from cgi import test
import importlib
from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.constant import *
from creditdefaulter.entity.model_entity import *
from creditdefaulter.util import util
from sklearn.metrics import classification_report,accuracy_score,confusion_matrix,roc_auc_score,f1_score

import os,sys
from typing import List
import numpy as np



class CreditDefaultEstimatorModel:
    def __init__(self, preprocessing_object, trained_model_object):
        """
        TrainedModel constructor
        preprocessing_object: preprocessing_object
        trained_model_object: trained_model_object
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, X):
        """
        function accepts raw inputs and then transformed raw input using preprocessing_object
        which gurantees that the inputs are in the same format as the training data
        At last it perform prediction on transformed features
        """
        transformed_feature = self.preprocessing_object.transform(X)
        return self.trained_model_object.predict(transformed_feature)

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"



class ModelFactory:

    def __init__(self,model_config_path:str = None):
        try:
            self.model_config = util.read_yaml_file(self.model_config_path)
            
            self.grid_search_class:str = self.model_config[GRID_SEARCH_CONFIG_KEY][GRID_SEARCH_CLASS_KEY]
            
            self.grid_search_module:str = self.model_config[GRID_SEARCH_CONFIG_KEY][GRID_SEARCH_MODULE_KEY]
            
            self.grid_search_params:dict = dict(self.model_config[GRID_SEARCH_CONFIG_KEY][GRID_SEARCH_PARAMS_KEY])
            
            self.model_initialization_config:dict = dict(self.model_config[MODEL_SELECTION_KEY])

            self.initialized_model_list = None
            self.grid_searched_best_model_list = None

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    @staticmethod
    def get_class_ref_from_name(module_name:str,class_name:str):
        try:
            module = importlib.import_module(module_name)

            logging.info(f"Executing Command from {module} import {class_name}")

            class_ref = getattr(module,class_name)

            return class_ref

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys)

    def update_property_of_class(instance_ref:object,property_details:dict):

        try:

            if not isinstance(property_details) == dict:
                raise Exception("To update property details in object need property details in the form of dictionary")
        
            for key,value in property_details.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref,key,value)

            return instance_ref
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def get_initialized_model_list(self) -> List[InitializedModelDetail]:
        try:
            model_inilialze_list = []
            
            for model_serial_no in self.model_initialization_config.keys():
                model_initalization_config = self.model_initialization_config[model_serial_no]
                model_obj_ref = self.get_class_ref_from_name(self.grid_search_module,self.grid_search_class)
                model = model_obj_ref()

                if GRID_SEARCH_PARAMS_KEY in self.model_initialization_config:
                    model_obj_property_data = self.model_initialization_config[MODEL_SELECTION_PARAMS_KEY]
                    model = ModelFactory.update_property_of_class(instance_ref= model,property_details=model_obj_property_data)

                param_grid_search = model_initalization_config[MODEL_SELECTION_SEARCH_PARAM_GRID_KEY]
                model_name = f"{self.grid_search_module}.{self.grid_search_class}"

                model_initialize_Config = InitializedModelDetail(model_serial_no=model_serial_no,
                                                                    model=model,
                                                                    param_grid_Search=param_grid_search,
                                                                    model_name=model_name)
                model_inilialze_list.append(model_initialize_Config)
            
            self.initialized_model_list = model_inilialze_list
            return self.initialized_model_list

        except Exception as e:
   
            raise Credit_Card_Default_Exception(e,sys) from e


    def grid_search_operations(self,initialized_model:InitializedModelDetail,input_feature,output_feature) ->GridSearchBestModel:
        try:
            grid_search_cv_ref =  self.get_class_ref_from_name(module_name=self.grid_search_module,class_name=self.grid_search_class)
            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model,param_grid = initialized_model.param_grid_Search)
            grid_search_cv = ModelFactory.update_property_of_class(instance_ref=grid_search_cv,
                                                                    property_details=self.grid_search_params)
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Started." {"<<"*30}'
            logging.info(message)
            grid_search_cv.fit(input_feature,output_feature)
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__}" completed {"<<"*30}'
            
            gridSearchBestModel = GridSearchBestModel(model_serial_no=initialized_model.model_serial_no,
                                                        model=initialized_model.model,
                                                        best_model=grid_search_cv.best_estimator_,
                                                        best_parameters=grid_search_cv.best_params_,
                                                        best_scores=grid_search_cv.best_score_)

            return gridSearchBestModel

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def initiate_best_parameter_search_for_best_model(self,initialized_model:InitializedModelDetail,input_feature,output_feature) -> GridSearchBestModel:
        try:
            return self.grid_search_operations(initialized_model=initialized_model,
                                            input_feature=input_feature,
                                            output_feature=output_feature)
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

   
    def initiate_best_parameter_search_for_best_models(self,initialized_model_list:List[InitializedModelDetail],input_feature,output_feature) -> List[GridSearchBestModel]:
   
        try:
            
            self.grid_searched_best_model_list = []
            for initialized_model in initialized_model_list:
                grid_searched_best_model = self.initiate_best_parameter_search_for_best_model(initialized_model=initialized_model,input_feature=input_feature,output_feature=output_feature)
                self.grid_searched_best_model_list.append(grid_searched_best_model)

            return self.grid_searched_best_model_list
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def get_best_model_from_grid_Search_best_model_list(GridSearchBestModellist : List[GridSearchBestModel],best_accuracy) -> BestModel:
        try:
            best_model = None

            for gridSearchBestModel in GridSearchBestModellist:

                if best_accuracy < gridSearchBestModel.best_scores:
                    logging.info(f"Acceptable model found:{gridSearchBestModel}")
                    best_accuracy = gridSearchBestModel.best_scores
                    best_model = gridSearchBestModel

            if not best_model:
                raise Exception(f"None of Model has base accuracy: {best_accuracy}")
                
            logging.info(f"Best model: {best_model}")

            return best_model

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
            

    def get_best_model(self,X,y,best_accuracy=0.6) ->BestModel:
        try:
            initialized_model_list = self.get_initialized_model_list()
            logging.info(f"initialized_model_list : {[initialized_model_list]}")

            gridSearchBestModellist = self.initiate_best_parameter_search_for_best_models(initialized_model_list=initialized_model_list,
                                                                    input_feature=X,
                                                                        output_feature=y)

            return self.get_best_model_from_grid_Search_best_model_list(GridSearchBestModellist = gridSearchBestModellist,
                                                                            best_accuracy = best_accuracy)

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def evaluate_classification_model(self,model_list:list,X_train:np.array,y_train:np.array, X_test:np.array,y_test:np.array,base_accuracy:float= 0.6) -> MetricInfoArtifact:
        try:
            index_number = 0
            metricInfoArtifact = None

            for model in model_list:
                model_name = str(model)  #getting model name based on model object
                y_train_pred = model.predict(X_train)
                y_test_pred = model.predict(X_test)

                train_accuracy = accuracy_score(y_train,y_train_pred)
                test_accuracy = accuracy_score(y_test,y_test_pred)

                tn_train, fp_train, fn_train, tp_train = confusion_matrix(y_train,y_train_pred).ravel()
                tn_test, fp_test, fn_test, tp_test = confusion_matrix(y_test,y_test_pred).ravel()

                recall_train = tp_train / (tp_train+fn_train)
                recall_test = tp_test / (tp_test+fn_test)

                precision_train = tp_train / (tp_train+fp_train)
                precision_test = tp_test / (tp_test+fp_test)

                f1_score_train = f1_score(y_train,y_train_pred)
                f1_score_test = f1_score(y_test,y_test_pred)

                roc_auc_score_train = roc_auc_score(y_train,y_train_pred)
                roc_auc_score_test = roc_auc_score(y_test,y_test_pred)

                model_accuracy = (2 * (train_accuracy * test_accuracy)) / (train_accuracy + test_accuracy)
                diff_test_train_acc = abs(test_accuracy - train_accuracy)

                if model_accuracy >= base_accuracy and diff_test_train_acc <= 0.05:
                    base_accuracy = model_accuracy

                    metricInfoArtifact = MetricInfoArtifact(model_name = model_name, 
                                                            model_object = model, 
                                                            train_accuracy = train_accuracy, 
                                                            test_accuracy = test_accuracy, 
                                                            model_accuracy = model_accuracy,
                                                            tp_train = tp_train,
                                                            tn_train = tn_train,
                                                            fn_train = fn_train,
                                                            fp_train = fp_train,
                                                            tp_test = tp_test,
                                                            tn_test = tn_test,
                                                            fn_test = fn_test,
                                                            fp_test = fp_test,
                                                            recall_train = recall_train,
                                                            recall_test = recall_test,
                                                            precision_train = precision_train,
                                                            precision_test = precision_test,
                                                            f1_score_train = f1_score_train,
                                                            f1_score_test = f1_score_test,
                                                            roc_auc_score_train = roc_auc_score_train,
                                                            roc_auc_score_test = roc_auc_score_test,
                                                            index_number = index_number)

                    logging.info(f"Acceptable model found {metricInfoArtifact}. ")

                index_number = index_number + 1


            if metricInfoArtifact is None:
                logging.info(f"No model found with higher accuracy than base accuracy")
                
            return metricInfoArtifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    