import shutil
from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.entity.config_entity import ModelPusherConfig
from creditdefaulter.entity.artifact_entity import ModelEvaluationArtifact, ModelPusherArtifact, ModelTrainerArtifact

import os,sys

class ModelPusher:

    def __init__(self,modelPusherConfig:ModelPusherConfig,modelEvaluationArtifact:ModelEvaluationArtifact):
        try:
            logging.info(f"{'<<'*10}Model Pusher Artifact Started {'>>'*10}")
            self.modelPusherConfig = modelPusherConfig
            self.modelEvaluationArtifact = modelEvaluationArtifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
    
    def export_model(self) -> ModelPusherArtifact:
        try:
            export_dir_path = self.modelPusherConfig.export_dir_path
            evaluated_model_path = self.modelEvaluationArtifact.evaluated_model_path

            model_name = os.path.basename(evaluated_model_path)

            export_model_file_path = os.path.join(export_dir_path,model_name)

            os.makedirs(export_model_file_path,exist_ok=True)

            shutil.copy(src=evaluated_model_path,dst=export_model_file_path)

            logging.info(f"Trained model: {evaluated_model_path} is copied in export dir:[{export_model_file_path}]")

            modelPusherArtifact=ModelPusherArtifact(is_model_pusher=True,export_model_file_path=export_model_file_path)

            logging.info(f"Model Pusher Artifact : {[modelPusherArtifact]}")

            return modelPusherArtifact

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e