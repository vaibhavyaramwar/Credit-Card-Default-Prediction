import yaml
from creditdefaulter.exception import Credit_Card_Default_Exception 

import os,sys
import numpy as np
import dill

def read_yaml_file(file_path:str):
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

def save_numpy_arr_data(file_path:str,numpy_arr:np.array):
    try:
        #if not os.path.exists(file_path):
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            np.save(file_obj,numpy_arr)
    
    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e

def save_obj(file_path:str,obj):
    try:
        
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise Credit_Card_Default_Exception(e,sys) from e