from sklearn.compose import ColumnTransformer
from creditdefaulter.logger import logging
from creditdefaulter.exception import Credit_Card_Default_Exception
from creditdefaulter.entity.config_entity import DataTransformationConfig
from creditdefaulter.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from creditdefaulter.constant import *
from creditdefaulter.util import util
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import OneHotEncoder,StandardScaler,PowerTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

from collections import namedtuple
import pandas as pd
import numpy as np
import statistics

import os,sys


FeatureBoudry = namedtuple("FeatureBoudry",["lb","ub"]) 

class OutlierImputationTransformation(BaseEstimator,TransformerMixin):
    
    def __init__(self):
        try:
            self.outlierBoudryDetails = dict()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def fit(self,training_df,y=None):
        try:
            for feature in training_df.columns:
                q1=np.percentile(a=training_df[feature],q=25)
                q3=np.percentile(a=training_df[feature],q=75)

                iqr = q3-q1
                lb = q1-1.5*iqr
                ub = q3+1.5*iqr

                outlier_exixts = len([x for x in training_df[feature] if x < lb or x > ub])

                if outlier_exixts > 0:
                    featureBoudry = FeatureBoudry(lb=lb,ub=ub)
                    self.outlierBoudryDetails[feature] = featureBoudry
                    
            return self

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def transform(self,df):
        try:
            for feature in self.outlierBoudryDetails.keys():
                boundryDetails = self.outlierBoudryDetails.get(feature)
                df.loc[df[feature] < boundryDetails.lb ,feature] = boundryDetails.lb
                df.loc[df[feature] > boundryDetails.ub ,feature] = boundryDetails.ub
                
            return df
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

class CategoricalCategoryTransformation(BaseEstimator,TransformerMixin):
    
    def __init__(self):
        try:
            self.mode_details = dict()
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def fit(self,X,y=None):
        try:
            for feature in X.columns:
                self.mode_details[feature] = statistics.mode(X[feature])

            return self
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def transform(self,X):
        try:
            for feature in X.columns:
    
                for value in X[feature].value_counts().index:
        
                    tot_perc = len(X[X[feature]==value])/X.shape[0]
                    if tot_perc < CATEGORICAL_COLUMN_THRESHOLD:
                        if feature in self.mode_details.keys():
                            X.loc[X[feature] == value, feature] = self.mode_details.get(feature)
                        else: 
                            raise Exception("Required column not exists in Training dataset hence mode would not be computed")

            return X
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                      data_ingestion_artifact:DataIngestionArtifact,
                      data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validationArtifact = data_validation_artifact
        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def get_data_transformation_object(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validationArtifact.schema_file_path
            schema_details = util.read_yaml_file(schema_file_path)
            numerical_columns = schema_details[NUMERICAL_COLUMN_KEY]
            categorical_columns = schema_details[CATEGORICAL_COLUMNS_KEY]

            num_pipeline = Pipeline(steps=[('imputer',SimpleImputer(strategy="median")),
                                           # ('outlier',OutlierImputationTransformation()),
                                            ('scaler',StandardScaler())
                                          #  ('powerTransformer',PowerTransformer(method="yeo-johnson"))
                                    ])

            cat_pipeline = Pipeline(steps=[#("categoricalCategoryTransformation",CategoricalCategoryTransformation()),
                                            ('impute', SimpleImputer(strategy="most_frequent")),
                                            ('oneHotEncoder',OneHotEncoder(handle_unknown="ignore")),
                                           ('scaling',StandardScaler(with_mean=False))
                                    ])

            preprocessing = ColumnTransformer([('num_pipeline',num_pipeline,numerical_columns),
                                    ('cat_pipeline',cat_pipeline,categorical_columns)])
            
            return preprocessing

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e


    def get_data_transformation_artifact(self,transformed_train_dir,transformed_test_dir,preprocessed_object_file_name,
                                              is_transformed,message) -> DataTransformationArtifact:
        try:

            

            data_transformation_artifact = DataTransformationArtifact(transformed_train_dir=transformed_train_dir,
                                                                        transformed_test_dir=transformed_test_dir,
                                                                        preprocessed_object_file_name=preprocessed_object_file_name,
                                                                        is_transformed=is_transformed,
                                                                        message=message)

            return data_transformation_artifact

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:

            preprocessing_obj = self.get_data_transformation_object()
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)

            schema_file_path = self.data_validationArtifact.schema_file_path

            schema = util.read_yaml_file(schema_file_path)

            target_column_name = TARGET_COLUMN_NAME

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]

           # outlierImputationTransformation = OutlierImputationTransformation()
           # outlierImputationTransformation.fit(input_feature_train_df,target_feature_train_df)
           # trans_train_df = outlierImputationTransformation.transform(input_feature_train_df)
           # trans_test_df = outlierImputationTransformation.transform(input_feature_test_df)

            logging.info(f"input_feature_train_df : {input_feature_train_df}")
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info(f"input_feature_train_arr : {input_feature_train_arr}")

            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"input_feature_train_arr:{input_feature_train_arr}")

            train_file_path = os.path.basename(train_file_path).replace(".csv",".npz")
            test_file_path = os.path.basename(test_file_path).replace(".csv",".npz")

            transformed_train_dir=self.data_transformation_config.transformed_train_dir
            transformed_test_dir=self.data_transformation_config.transformed_test_dir
            
            transformed_train_file_path = os.path.join(transformed_train_dir,train_file_path) 
            transformed_test_file_path = os.path.join(transformed_test_dir,test_file_path)

            util.save_numpy_arr_data(transformed_train_file_path,train_arr)
            util.save_numpy_arr_data(transformed_test_file_path,test_arr)

            preprocessing_obj_file_path = self.data_transformation_config.preprocessed_object_file_name

            util.save_obj(file_path=preprocessing_obj_file_path,obj=preprocessing_obj)

            data_transformation_artifact =  self.get_data_transformation_artifact(transformed_train_dir=transformed_train_file_path,transformed_test_dir=transformed_test_file_path,
            preprocessed_object_file_name=preprocessing_obj_file_path,is_transformed=True,message="Data Transformation Successful")

            logging.info(f"Data Transformation Artifact : [{data_transformation_artifact}]")

            return data_transformation_artifact

        except Exception as e:
            raise Credit_Card_Default_Exception(e,sys) from e