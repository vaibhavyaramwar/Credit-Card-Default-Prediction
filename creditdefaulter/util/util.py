from typing import Dict
import yaml
from creditdefaulter.constant import COLUMNS_KEY, TARGET_COLUMN_NAME
from creditdefaulter.exception import Credit_Card_Default_Exception 

import os,sys
import numpy as np
import pandas as pd
import dill


def read_yaml_file(file_path:str) -> dict:
    try:
        '''
            This function is used to read the yaml file
            Input params : 
            file_path : str : This is yaml file path where all the pipeline configurations exists
        '''
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)

    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

def load_data(file_path:str,schema_file_path:str) -> pd.DataFrame:
    try:
        schema = read_yaml_file(file_path=schema_file_path)
        columns=schema[COLUMNS_KEY]

        df = pd.read_csv(file_path)

        error_message = ""
        for feature in df.columns:

            if feature not in TARGET_COLUMN_NAME:
                if feature in columns.keys():
                    df[feature].astype(columns[feature])
                else:
                    error_messgae = f" \nColumn: [{feature}] is not in the schema."

            if len(error_message) > 0:
                raise Exception(error_messgae)

        return df

    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

def save_numpy_arr_data(file_path:str,numpy_arr:np.array):
    try:
        #if not os.path.exists(file_path):
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            np.save(file_obj,numpy_arr,allow_pickle=True)
    
    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e



def load_numpy_arr_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj,allow_pickle=True)
    except Exception as e:
        raise Credit_Card_Default_Exception(e, sys) from e

def save_obj(file_path:str,obj):
    try:
        
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

def load_obj(file_path:str):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

def write_yaml_file(file_path:str,data:dict = None):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)


    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e