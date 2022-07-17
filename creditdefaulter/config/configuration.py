from creditdefaulter.constant import * 
from creditdefaulter.util import util
from creditdefaulter.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
import sys

class Configuration:

    def __init__(self,config_file_path:str = CONFIG_FILE_PATH,
                        current_time_stamp:str = CURRENT_TIME_STAMP):
        self.config_info = util.read_yaml_file(config_file_path)
        self.training_pipeline_config = self.get_Training_Pipeline_Config()
        self.time_stamp =  current_time_stamp


    def get_Training_Pipeline_Config(self) -> TrainingPipelineConfig:
        try:
            training_pipline_config_key = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            pipelinename = training_pipline_config_key[TRAINING_PIPELINE_NAME_KEY]
            artifact_dir = training_pipline_config_key[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]

            artifact_dir_path = os.path.join(ROOT_DIR,pipelinename,artifact_dir)

            training_pipeline_config = TrainingPipelineConfig(name=pipelinename,artifact_dir=artifact_dir_path)

            logging.info(f"Training Pipeline Config : {[training_pipeline_config]}")

            return training_pipeline_config

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config_key = self.config_info[DATA_INGESTION_CONFIG_KEY]
            data_ingestion_artifact_dir = DATA_INGESTION_ARTIFACT_DIR
            data_ingestion_artifact_dir_path = os.path.join(self.training_pipeline_config.artifact_dir,data_ingestion_artifact_dir,self.time_stamp)
            
            download_file_name = data_ingestion_config_key[DATA_INGESTION_DATASET_DOWNLOAD_FILE_NAME_KEY]
            raw_data_dir = os.path.join(data_ingestion_artifact_dir_path,data_ingestion_config_key[DATA_INGESTION_RAW_DATA_DIR_KEY])
            extracted_download_dir = os.path.join(data_ingestion_artifact_dir_path,data_ingestion_config_key[DATA_INGESTION_EXTRACTED_DOWNLOAD_DIR_KEY])
            #ingested_dir = data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_KEY]
            ingested_dir = data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_KEY]
            
            
            ingested_train_dir = os.path.join(data_ingestion_artifact_dir_path,data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_KEY],data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_TRAIN_DIR_KEY])
            ingested_test_dir = os.path.join(data_ingestion_artifact_dir_path,data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_KEY],data_ingestion_config_key[DATA_INGESTION_INGESTED_DIR_TEST_DIR_KEY])

            data_ingestion_config = DataIngestionConfig(artifact_dir_path=data_ingestion_artifact_dir_path,
                                                        dataset_download_file_name=download_file_name,
                                                        raw_data_dir=raw_data_dir,
                                                        extracted_download_dir=extracted_download_dir,
                                                        ingested_train_dir=ingested_train_dir,
                                                        ingested_test_dir=ingested_test_dir)

            logging.info(f"Data Ingestion Config : {[data_ingestion_config]}")

            return data_ingestion_config

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config_key = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            data_validation_artifact_dir = DATA_VALIDATION_ARTIFACT_DIR_NAME
            data_validation_artifact_dir_path = os.path.join(self.training_pipeline_config.artifact_dir,data_validation_artifact_dir,self.time_stamp)

            schema_dir = data_validation_config_key[DATA_VALIDATION_SCHEMA_DIR_KEY]
            schema_dir_file = data_validation_config_key[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            schema_file_path = os.path.join(schema_dir,schema_dir_file)

            report_file_name = data_validation_config_key[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            report_file_name_path = os.path.join(data_validation_artifact_dir_path,report_file_name)

            report_page_file_name = data_validation_config_key[DATA_VALIDATION_REPORT_FILE_PATH_NAME_KEY]
            report_page_file_name_path = os.path.join(data_validation_artifact_dir_path,report_page_file_name)

            data_validation_config = DataValidationConfig(artifact_dir_path=data_validation_artifact_dir_path,
                                                            schema_dir=schema_dir,
                                                            schema_file_path=schema_file_path,
                                                            report_file_name_path=report_file_name_path,
                                                            report_page_file_path_name=report_page_file_name_path)

            logging.info(f"Data Validation Config : {[data_validation_config]}")

            return data_validation_config

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e