from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
from creditdefaulter.util import util
from creditdefaulter.constant import *
from creditdefaulter.entity.config_entity import ModelEvaluationConfig 
from creditdefaulter.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from creditdefaulter.entity.model_entity import MetricInfoArtifact
from creditdefaulter.entity.model_factory import ModelFactory

import os,sys
import numpy as np
import yaml

class ModelEvaluation:

    def __init__(self,modelEvaluationConfig:ModelEvaluationConfig,
                        dataIngestionArtifact:DataIngestionArtifact,
                        dataValidationArtifact:DataValidationArtifact,
                        modelTrainerArtifact:ModelTrainerArtifact
                        ):
        try:
            logging.info(f"{'>>' * 30}Model Evaluation log started.{'<<' * 30} ")
            self.modelEvaluationConfig = modelEvaluationConfig
            self.dataIngestionArtifact = dataIngestionArtifact
            self.dataValidationArtifact = dataValidationArtifact
            self.modelTrainerArtifact = modelTrainerArtifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_name_path = self.modelEvaluationConfig.model_evaluation_file_name_path

            if not os.path.exists(model_evaluation_file_name_path):
                util.write_yaml_file(file_path=model_evaluation_file_name_path,)
                return model

            model_evaluation_file_content = util.read_yaml_file(file_path=model_evaluation_file_name_path)

            if model_evaluation_file_content is None:
                model_evaluation_file_content = dict()
            
            if BEST_MODEL_KEY not in model_evaluation_file_content:
                return model
            
            model = util.load_obj(file_path=model_evaluation_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])

            return model

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def update_evaluation_report(self,modelEvaluationArtifact:ModelEvaluationArtifact):
        try:
            evaluated_model_path = self.modelEvaluationConfig.model_evaluation_file_name_path
            trained_model_file_path = self.modelTrainerArtifact.trained_model_file_path

            model_avaluation_content = util.read_yaml_file(file_path=evaluated_model_path)
            model_avaluation_content = dict() if model_avaluation_content is None else model_avaluation_content

            previous_best_model = None
            if BEST_MODEL_KEY in model_avaluation_content:
                previous_best_model = model_avaluation_content[BEST_MODEL_KEY]

            eval_result = {
                BEST_MODEL_KEY : {
                    MODEL_PATH_KEY : modelEvaluationArtifact.evaluated_model_path
                }
            }

            if previous_best_model is not None:
                model_history = {self.modelEvaluationConfig.time_stamp:previous_best_model}

                if HISTORY_KEY not in model_avaluation_content:
                    history = {HISTORY_KEY:model_history}
                    eval_result.update(history)
                else:
                    model_avaluation_content[HISTORY_KEY].update(model_history)


            model_avaluation_content.update(eval_result)

            util.write_yaml_file(file_path=self.modelEvaluationConfig.model_evaluation_file_name_path,data=model_avaluation_content)

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.modelTrainerArtifact.trained_model_file_path
            model_object = util.load_obj(file_path=trained_model_file_path)

            train_file_path=self.dataIngestionArtifact.train_file_path
            test_file_path=self.dataIngestionArtifact.test_file_path

            schema_file_path = self.dataValidationArtifact.schema_file_path

            schema=util.read_yaml_file(file_path=schema_file_path)

            target_column = TARGET_COLUMN_NAME

            train_df = util.load_data(file_path=train_file_path,schema_file_path=schema_file_path)
            test_df = util.load_data(file_path=test_file_path,schema_file_path=schema_file_path)

            train_target_arr = np.array(train_df[target_column])
            test_target_arr = np.array(test_df[target_column])

            train_df.drop(target_column,axis=1,inplace=True)
            test_df.drop(target_column,axis=1,inplace=True)

            model = self.get_best_model()

            if model is None:
                modelEvaluationArtifact = ModelEvaluationArtifact(is_model_accepted=True,evaluated_model_path=trained_model_file_path)
                self.update_evaluation_report(modelEvaluationArtifact=modelEvaluationArtifact)

                return modelEvaluationArtifact

            #print("model_object : ",type(model_object))
            #print("model : ",type(model))
            model_list = [model,model_object] 

            #print("model_list : ",model_list)

            metricInfoArtifact:MetricInfoArtifact = ModelFactory.evaluate_classification_model(model_list,train_df,train_target_arr, test_df,test_target_arr,self.modelTrainerArtifact.model_accuracy)

            if metricInfoArtifact is None:
                modelEvaluationArtifact=ModelEvaluationArtifact(is_model_accepted=False,
                                                        evaluated_model_path=trained_model_file_path)
                return modelEvaluationArtifact

            if metricInfoArtifact.index_number == 1:
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                                        is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model eval artifact {model_evaluation_artifact} created")
            else:
                logging.info("Trained model is no better than existing model hence not accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                        is_model_accepted=False)

            return model_evaluation_artifact

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} ")