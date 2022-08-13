from threading import Thread
from creditdefaulter.component.data_transformation import DataTransformation
from creditdefaulter.component.data_validation import DataValidation
from creditdefaulter.component.model_evaluation import ModelEvaluation
from creditdefaulter.component.model_pusher import ModelPusher
from creditdefaulter.component.model_trainer import ModelTrainer
from creditdefaulter.constant import EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME
from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.config.configuration import Configuration
from creditdefaulter.entity.config_entity import *
from creditdefaulter.entity.artifact_entity import *
from creditdefaulter.entity.experiment_entity import Experiment
from creditdefaulter.component.data_ingestion import DataIngestion 
import sys
import os

from datetime import datetime
import uuid
import pandas as pd

class Pipeline(Thread):

    experiment: Experiment = Experiment(*([None] * 11))
    experiment_file_path = None

    def __init__(self,configuration:Configuration=Configuration()):
        
        os.makedirs(configuration.training_pipeline_config.artifact_dir,exist_ok=True)
        Pipeline.experiment_file_path = os.path.join(configuration.training_pipeline_config.artifact_dir,EXPERIMENT_DIR_NAME,EXPERIMENT_FILE_NAME)
        #super.__init__(daemon=False,name="pipeline")
        self.configuration = configuration

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            
            data_ingestion_config = self.configuration.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        try:
            data_validation_config = self.configuration.get_data_validation_config()
            data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,
                                        data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation_config = self.configuration.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config=data_transformation_config,
                                                        data_ingestion_artifact=data_ingestion_artifact,
                                                        data_validation_artifact=data_validation_artifact)

            return data_transformation.initiate_data_transformation()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e  

    def start_model_training(self,data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            
            model_trainer_config = self.configuration.get_model_trainer_config()
            
            modelTrainer = ModelTrainer(model_trainer_config=model_trainer_config,
                                         data_transformation_artifact=data_transformation_artifact)

            return modelTrainer.initiate_model_trainer()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def start_model_evaluation(self,dataIngestionArtifact:DataIngestionArtifact,dataValidationArtifact:DataValidationArtifact,modelTrainerArtifact:ModelTrainerArtifact) -> ModelEvaluationArtifact:
        try:
            model_evaluation_config = self.configuration.get_model_evaluation_config()

            modelEvaluation = ModelEvaluation(modelEvaluationConfig=model_evaluation_config,
                                                dataIngestionArtifact=dataIngestionArtifact,
                                                dataValidationArtifact=dataValidationArtifact,
                                                modelTrainerArtifact=modelTrainerArtifact)

            return modelEvaluation.initiate_model_evaluation()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
                                    
    def start_model_pusher(self,modelEvaluationArtifact:ModelEvaluationArtifact) -> ModelPusherArtifact:
        try:
            model_pusher_config = self.configuration.get_model_pusher_config()
            modelEvaluationArtifact = modelEvaluationArtifact

            modelPusher = ModelPusher(modelPusherConfig=model_pusher_config,modelEvaluationArtifact=modelEvaluationArtifact)
            return modelPusher.initiate_model_pusher()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e                                        

    '''
    def run_pipeline(self):
        try:
            if Pipeline.experiment.running_status:
                logging.info("Pipeline is already running")
                return Pipeline.experiment

            logging.info("Pipeline starting.")
            experiment_id = str(uuid.uuid4())
            Pipeline.experiment = Experiment(experiment_id=experiment_id,
                                 initialization_timestamp=self.config.time_stamp,
                                 artifact_time_stamp=self.config.time_stamp,
                                 running_status=True,
                                 start_time=datetime.now(),
                                 stop_time=None,
                                 execution_time=None,
                                 experiment_file_path=Pipeline.experiment_file_path,
                                 is_model_accepted=None,
                                 message="Pipeline has been started.",
                                 accuracy=None,
                                 )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            
            self.save_experiment()

            dataIngestionArtifact = self.start_data_ingestion()
            dataValidationArtifact =  self.start_data_validation(data_ingestion_artifact=dataIngestionArtifact)
            dataTransformationArtifact = self.start_data_transformation(data_ingestion_artifact= dataIngestionArtifact,
                                                                        data_validation_artifact= dataValidationArtifact)
            modelTrainerArtifact = self.start_model_training(data_transformation_artifact=dataTransformationArtifact)

            modelEvaluationArtifact = self.start_model_evaluation(dataIngestionArtifact=dataIngestionArtifact,
                                            dataValidationArtifact=dataValidationArtifact,
                                            modelTrainerArtifact=modelTrainerArtifact)        

            if modelEvaluationArtifact.is_model_accepted:
                modelPusherArtifact = self.start_model_pusher(modelEvaluationArtifact)
            else:
                logging.info("Training Model Rejected")

            stop_time = datetime.now()
            Pipeline.experiment = Experiment(experiment_id=Pipeline.experiment.experiment_id,
                                 initialization_timestamp=self.config.time_stamp,
                                 artifact_time_stamp=self.config.time_stamp,
                                 running_status=False,
                                 start_time=Pipeline.experiment.start_time,
                                 stop_time=stop_time,
                                 execution_time=stop_time - Pipeline.experiment.start_time,
                                 message="Pipeline has been completed.",
                                 experiment_file_path=Pipeline.experiment_file_path,
                                 is_model_accepted=modelEvaluationArtifact.is_model_accepted,
                                 accuracy=modelTrainerArtifact.model_accuracy
                                 )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    '''

    def save_experiment(self):
        try:
            if self.experiment.running_status is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict : dict = {key : [value] for key,[value] in experiment_dict.items()}
                experiment_dict.update({"created_time_stamp": [datetime.now()],
                                        "experiment_file_path": [os.path.basename(Pipeline.experiment.experiment_file_path)]})

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok=True)
                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index=False, header=False, mode="a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, mode="w", index=False, header=True)

            else:
                logging.info("Experiment is not yet started")
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    
    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys)

    @classmethod
    def get_experiment_status(cls,limit:int=5) -> pd.DataFrame:
    
        if os.path.exists(Pipeline.experiment_file_path):
            df = pd.read_csv(Pipeline.experiment_file_path)
            df = df[-1*int(limit),]
            df.drop(columns=["experiment_file_path", "initialization_timestamp"],axis=1,inplace=True)
            return df
        else:
            return pd.DataFrame




    def run_pipeline(self):
        try:          
            dataIngestionArtifact = self.start_data_ingestion()
            dataValidationArtifact =  self.start_data_validation(data_ingestion_artifact=dataIngestionArtifact)
            dataTransformationArtifact = self.start_data_transformation(data_ingestion_artifact= dataIngestionArtifact,
                                                                        data_validation_artifact= dataValidationArtifact)
            modelTrainerArtifact = self.start_model_training(data_transformation_artifact=dataTransformationArtifact)

            modelEvaluationArtifact = self.start_model_evaluation(dataIngestionArtifact=dataIngestionArtifact,
                                            dataValidationArtifact=dataValidationArtifact,
                                            modelTrainerArtifact=modelTrainerArtifact)        

            if modelEvaluationArtifact.is_model_accepted:
                modelPusherArtifact = self.start_model_pusher(modelEvaluationArtifact)
            else:
                logging.info("Training Model Rejected")

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
