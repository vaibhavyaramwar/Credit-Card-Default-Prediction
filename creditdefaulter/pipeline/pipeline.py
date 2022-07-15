from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.config.configuration import Configuration
from creditdefaulter.entity.config_entity import *
from creditdefaulter.entity.artifact_entity import *
from creditdefaulter.component.data_ingestion import DataIngestion 
import sys
import os

class Pipeline:

    def __init__(self,configuration:Configuration=Configuration()):
        self.configuration = configuration

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            
            data_ingestion_config = self.configuration.get_data_ingestion_config()
            data_ingestion = DataIngestion(data_ingestion_config)
            data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def run_pipeline(self):
        try:          
            self.start_data_ingestion()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
