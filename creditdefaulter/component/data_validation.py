from typing import List
from xmlrpc.client import Boolean

from traitlets import Bool
from creditdefaulter.config.configuration import DataValidationConfig
from creditdefaulter.constant import TOTAL_COLUMNS
from creditdefaulter.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
from creditdefaulter.util import util
from creditdefaulter.constant import *

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

import os,sys
import pandas as pd
import json

class DataValidation:

    def __init__(self,data_validation_config:DataValidationConfig,
                        data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'*'*20} Data Validation Log Started {'*'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e   
   

    def is_train_test_file_exists(self) -> Boolean:
        
        train_file_path = self.data_ingestion_artifact.train_file_path
        test_file_path = self.data_ingestion_artifact.test_file_path
        is_train_test_exists = True       
        is_available = os.path.exists(train_file_path) and os.path.exists(test_file_path)

        if not is_available:
            is_train_test_exists = False

        return is_train_test_exists 

    def get_data_validation_artifact(self,schema_file_path,report_file_path,report_page_file_path,is_validated,message) -> DataValidationArtifact:
        
        try:
            data_validation_artifact = DataValidationArtifact(schema_file_path=schema_file_path,
                                                                report_file_path=report_file_path,
                                                                report_page_file_path=report_page_file_path,
                                                                is_validated=is_validated,
                                                                message=message)

            return data_validation_artifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def get_train_test_df(self) :
        try:
            
            training_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

           # print("training_file_path : ",training_file_path)
           # train_file = os.listdir(training_file_path)[0]
           # test_file = os.listdir(test_file_path)[0]

            train_file_derived_path = os.path.join(training_file_path,training_file_path)
            test_file_derived_path = os.path.join(test_file_path,test_file_path)

            train_df = pd.read_csv(train_file_derived_path)
            test_df = pd.read_csv(test_file_derived_path)

            return train_df,test_df


        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def read_schema_file(self) -> list:
        try:
             schema = util.read_yaml_file(self.data_validation_config.schema_file_path)
             schema_columns = schema[COLUMNS_ORDER_KEY]
             return schema_columns
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def validate_column_names(self,validate_df:pd.DataFrame) -> Boolean:
        try:
            
            schema_columns = self.read_schema_file()
            validate_df_columns=list(validate_df.columns)
            validate_df_columns=validate_df_columns[:-1]

            is_valid = True

            for result in range(0,len(schema_columns)-1):

                if schema_columns[result] == validate_df_columns[result]:
                    pass
                else:
                    is_valid = False
                    break

            return is_valid

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def validate_domain_values(self,validate_df:pd.DataFrame):
        try:
            schema = util.read_yaml_file(self.data_validation_config.schema_file_path)
            domain_value_key = schema[DOMAIN_VALUE_KEY]
            categorical_columns = schema[CATEGORICAL_COLUMNS_KEY]
            features_non_domain_values= []
            is_valid_domain_values = True
            for feature in categorical_columns:
                feature_unique_values_from_df = list(validate_df[feature].unique())
                domain_value_key_data = domain_value_key[feature]
                for values in feature_unique_values_from_df: 
                    if values not in domain_value_key_data:
                        features_non_domain_values.add(f"{feature} has value {values} which is not allowed as per schema defination , allowed values as per schema defination for feature : {feature} is {[domain_value_key_data]}")
                        is_valid_domain_values = False


                return features_non_domain_values,is_valid_domain_values
                
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df,test_df = self.get_train_test_df()
            profile.calculate(train_df,test_df)
            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_name_path
            report_dir_name = os.path.dirname(self.data_validation_config.report_file_name_path)
            os.makedirs(report_dir_name,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file,indent=6)

            return report

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df=self.get_train_test_df()
            dashboard.calculate(train_df,test_df)
            
            report_page_file_path = self.data_validation_config.report_page_file_path_name
            report_page_path_dir_name = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_path_dir_name,exist_ok=True)
            dashboard.save(report_page_file_path)

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e    


    def is_data_drift_found(self):
        try:

            report = self.save_data_drift_report()
            self.save_data_drift_report_page()
            is_data_drift = report[DATA_VALIDATION_DATA_DRIFT_KEY][DATA_VALIDATION_DATA_DRIFT_DATA_KEY][DATA_VALIDATION_DATA_DRIFT_DATA_METRICS_KEY][DATA_VALIDATION_DATA_DRIFT_DATA_METRICS_DATASETDRIFT_KEY]

            return is_data_drift
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Initiate Data Validation Log Started")

            schema_file_path = self.data_validation_config.schema_file_path 
            report_file_path = self.data_validation_config.report_file_name_path
            report_page_file_path = self.data_validation_config.report_page_file_path_name
            is_validated = False
            message = ""
            data_validation_artifact:DataValidationArtifact = None

            if self.is_train_test_file_exists():
                
                train_df,test_df = self.get_train_test_df()
                train_column_len = len(train_df.columns)
                test_column_len = len(test_df.columns)

                if train_column_len == TOTAL_COLUMNS and test_column_len == TOTAL_COLUMNS:
                    
                    if self.validate_column_names(train_df) and self.validate_column_names(test_df):
                        
                        features_non_domain_values_train,is_valid_domain_values_train = self.validate_domain_values(train_df)
                        features_non_domain_values_test,is_valid_domain_values_test = self.validate_domain_values(test_df)
                        
                        if is_valid_domain_values_train and  is_valid_domain_values_test:
                            
                            is_data_drift = self.is_data_drift_found()

                            if is_data_drift:
                                 message = f"Data Drift Found : Kindly refer Data Drift Report at path : {self.data_validation_config.report_file_name_path} and Data Drift Report Page : {self.data_validation_config.report_page_file_path_name}"
                                 data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                                 logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                                 return data_validation_artifact
                            else:
                                is_validated = True
                                message = f"Data Validation Perfomred Successfully"
                                data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                                logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                                return data_validation_artifact
                        else:
                            message = f"Domain Values are not validated : Train Domain Values Validation : {[features_non_domain_values_train]} , Test Domain Values Validation : {[features_non_domain_values_test]}"
                            data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                            logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                            return data_validation_artifact
                    else:
                        schema_columns = self.read_schema_file()
                        message = f"Column Names of Train and Test Datasets are not Validated with Schema Column Names : Train Columns : {[list(train_df.columns)]} Test Columns : {[list(test_df.columns)]} Schema Columns : {[schema_columns]}"
                        data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                        logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                        return data_validation_artifact
                else:
                     message = f"Required Column Not Match with Train and Test Dataset , Train Dataset Column Length : {train_column_len} , Test Dataset Column Length : {test_column_len} , Required Columns : {TOTAL_COLUMNS}"
                     data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                     logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                     return data_validation_artifact
            else:
                message = f"Train File Path : {self.data_ingestion_artifact.train_file_path} and Test File Path : {self.data_ingestion_artifact.test_file_path} are not exist"
                data_validation_artifact = self.get_data_validation_artifact(schema_file_path,report_file_path,report_page_file_path,is_validated,message)
                logging.info(f"Data Validation Artifact : {[data_validation_artifact]}")
                return data_validation_artifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e