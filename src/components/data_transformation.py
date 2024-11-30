import sys # provides access to system specific parameter and funcs, used to interact with Python runtime env
from dataclasses import dataclass
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer #used to create the pipeline
from sklearn.impute import SimpleImputer # to impute missing values
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object # jsut used for saving the pickle fil

import os

#We just want the input to the DataTransformationConfig
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join("artifacts","preprocessor.pkl") #Create models and want to save in a pkl file


class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            #numerical features
            numerical_columns = ["writing score","reading score"]

            categorical_columns = [
                "gender",
                "race/ethnicity",
                "parental level of education",
                "lunch",
                "test preparation course"
            ]

            #pipeline
            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median"))
                    ,("scaler",StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="most_frequent"))
                    ,("one_hot_encoder",OneHotEncoder())
                    ,("scaler",StandardScaler(with_mean=False))
                ]

            )
            logging.info("Categorical Columns: {categorical_columns}")
            logging.info("Numerical columns: {numerical_columns}")

            #ColumnTransformer
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("cat_pipeline",cat_pipeline,categorical_columns)
                ]
            )
            
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):


        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            


            logging.info("Train and Test data successfully read")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj = self.get_data_transformer_object()

            target_column_name = "math score"
            numerical_columns = ["writing score","reading score"]

            input_feature_train_df = train_df.drop(columns = [target_column_name],axis = 1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns = [target_column_name],axis = 1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.fit_transform(input_feature_test_df)


            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]

            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object")

            #we write this function save_object in utils
            save_object(
                #to save the pickle file
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)