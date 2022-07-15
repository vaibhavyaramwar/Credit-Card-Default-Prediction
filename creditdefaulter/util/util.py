import yaml
from creditdefaulter.exception import Credit_Card_Default_Exception 

import os,sys

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