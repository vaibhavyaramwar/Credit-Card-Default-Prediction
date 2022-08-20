from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.entity.config_entity import DataIngestionConfig
from creditdefaulter.entity.artifact_entity import *
from creditdefaulter.constant import *
from zipfile import ZipFile
import os,sys
from kaggle.api.kaggle_api_extended import KaggleApi
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
from imblearn.over_sampling import SMOTE

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            logging.info(f"{'*'*20} Data Ingestion Log Started {'*'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def extract_credit_card_default_data(self,raw_data_dir:str,extract_data_dir:str):
        try:
            if not os.path.exists(extract_data_dir):
                os.makedirs(extract_data_dir,exist_ok=True)

            with ZipFile(raw_data_dir,"r") as zip_file:
                zip_file.extractall(extract_data_dir)

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def download_credit_card_default_data(self):
        try:
            #os.environ[KAGGLE_USERNAME] = KAGGLE_USERNAME_VALUE
            #os.environ[KAGGLE_KEY] = KAGGLE_KEY_VALUE

            os.environ['KAGGLE_USERNAME'] = "vaibhavyaramwar" # username from the json file
            os.environ['KAGGLE_KEY'] = "d06d519f9650b21805c3e7b5c33e63c9" # key from the json file


            api = KaggleApi()
            api.authenticate()

            raw_data_dir=self.data_ingestion_config.raw_data_dir
            extract_data_dir = self.data_ingestion_config.extracted_download_dir

            if not os.path.exists(raw_data_dir):
                os.makedirs(raw_data_dir,exist_ok=True)

            api.dataset_download_files(self.data_ingestion_config.dataset_download_file_name, raw_data_dir)
        
            raw_data_file = os.listdir(raw_data_dir)[0]
            raw_data_dir_path = os.path.join(raw_data_dir,raw_data_file)
            
            self.extract_credit_card_default_data(raw_data_dir=raw_data_dir_path,extract_data_dir=extract_data_dir)

            return extract_data_dir

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def train_test_split(self,extract_data_dir:str) -> DataIngestionArtifact:
        try:
            
            extracted_files = os.listdir(extract_data_dir)
            file_name = extracted_files[0]
            extracted_file_path =os.path.join(extract_data_dir,file_name)

            credit_card_defaulter = pd.read_csv(extracted_file_path)

            total_positive_records = credit_card_defaulter[TARGET_COLUMN_NAME].value_counts()[1]
            total_records = credit_card_defaulter[TARGET_COLUMN_NAME].shape[0]

            imbalanced_ratio = round((total_positive_records / total_records),2)

            if imbalanced_ratio <= IMBALANCED_THRESHOLD:
                is_imbalanced = True
            else:
                is_imbalanced = False

      
            split = StratifiedShuffleSplit(n_splits=1,test_size=0.3,random_state=40)
            
            strat_train_df = None
            strat_test_df = None

            for train_index,test_index in split.split(credit_card_defaulter,credit_card_defaulter[TARGET_COLUMN_NAME]):
                strat_train_df = credit_card_defaulter.iloc[train_index]
                strat_test_df = credit_card_defaulter.iloc[test_index]

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,file_name)

            if strat_train_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                
                
                smote = SMOTE(random_state=42)
                X_train, y_train = smote.fit_resample(strat_train_df.drop(columns=TARGET_COLUMN_NAME,axis=1), strat_train_df[TARGET_COLUMN_NAME])
                strat_train_df = pd.concat([X_train, y_train],axis=1)
                             
                strat_train_df.to_csv(train_file_path,index=False)
            
            if strat_test_df is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
                strat_test_df.to_csv(test_file_path,index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_imbalanced=is_imbalanced,
                                                            imbalenced_ratio=imbalanced_ratio,
                                                            imbalanced_threshold=IMBALANCED_THRESHOLD,
                                                            is_ingested=True,
                                                            message="Data Ingestion Pipeline Successfully Completed")
            
            logging.info(f"Data Ingestion Artifact : [{data_ingestion_artifact}]")

            return data_ingestion_artifact

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            extract_data_dir = self.download_credit_card_default_data()
            return self.train_test_split(extract_data_dir)
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
