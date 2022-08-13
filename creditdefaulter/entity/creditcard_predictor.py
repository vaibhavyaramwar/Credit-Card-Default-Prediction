from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.logger import logging
from creditdefaulter.util import util
from creditdefaulter.constant import *

import os
import sys
import pandas as pd

class CreditCardData:

    def __init__(self,  id: int,limit_bal: float,sex: str,education: str,
                        marriage: str,age: int,pay_0: str,pay_2: str,
                        pay_3: str,pay_4: str,pay_5: str,
                        pay_6: str,bill_amt1: float,bill_amt2: float,
                        bill_amt3: float,bill_amt4: float,bill_amt5: float,
                        bill_amt6: float,pay_amt1: float,pay_amt2: float,
                        pay_amt3: float,pay_amt4: float,pay_amt5: float,
                        pay_amt6: float,default_payment_next_month: str = None):


                        try:
                            
                            self.id = id
                            self.limit_bal = limit_bal
                            self.sex = sex
                            self.education= education
                            self.marriage = marriage
                            self.age = age
                            self.pay_0 = pay_0 
                            self.pay_2 = pay_2 
                            self.pay_3 = pay_3 
                            self.pay_4 = pay_4 
                            self.pay_5 = pay_5 
                            self.pay_6 = pay_6
                            self.bill_amt1 = bill_amt1
                            self.bill_amt2 = bill_amt2
                            self.bill_amt3 = bill_amt3
                            self.bill_amt4 = bill_amt4
                            self.bill_amt5 = bill_amt5
                            self.bill_amt6 = bill_amt6
                            self.pay_amt1 = pay_amt1
                            self.pay_amt2 = pay_amt2
                            self.pay_amt3 = pay_amt3
                            self.pay_amt4 = pay_amt4
                            self.pay_amt5 = pay_amt5
                            self.pay_amt6 = pay_amt6
                            self.default.payment.next.month = default_payment_next_month
                        
                        except Exception as e:
                            raise Credit_Card_Default_Exception(e,sys) from e 


    def get_credit_card_Data_frame(self) -> pd.DataFrame:
        try:
            credit_Card_Data = self.get_credit_card_data_as_dict()
            return pd.DataFrame(credit_Card_Data)
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e
    
    def get_credit_card_data_as_dict(self):
        try:
            input_data = {

               "id": [self.id],
               "limit_bal": [self.limit_bal],
               "sex": [self.sex],
               "education": [self.education],
               "marriage": [self.marriage],
               "age": [self.age],
               "pay_0": [self.pay_0],
               "pay_2": [self.pay_2],
               "pay_3": [self.pay_3],
               "pay_4": [self.pay_4],
               "pay_5": [self.pay_5],
               "pay_6": [self.pay_6],
               "bill_amt1": [self.bill_amt1],
               "bill_amt2": [self.bill_amt2],
               "bill_amt3": [self.bill_amt3],
               "bill_amt4": [self.bill_amt4],
               "bill_amt5": [self.bill_amt5],
               "bill_amt6": [self.bill_amt6],
               "pay_amt1": [self.pay_amt1],
               "pay_amt2": [self.pay_amt2],
               "pay_amt3": [self.pay_amt3],
               "pay_amt4": [self.pay_amt4],
               "pay_amt5": [self.pay_amt5],
               "pay_amt6": [self.pay_amt6]
            }

            return input_data
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


class CreditCardPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise Credit_Card_Default_Exception(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise Credit_Card_Default_Exception(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = util.load_object(file_path=model_path)
            default_payment_next_month = model.predict(X)
            return default_payment_next_month
        except Exception as e:
            raise Credit_Card_Default_Exception(e, sys) from e