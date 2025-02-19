#Will have common functionalities

import os
import sys


import numpy as np 
import pandas as pd 

from src.exception import CustomException

import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

#Creating the function save_object that will be called in data_transformation , can be used
#elsewhere too

def save_object(file_path,obj):
    try:
        dir_path = os.path.dirname(file_path) #make a dir

        os.makedirs(dir_path,exist_ok = True)

        with open(file_path,"wb") as file_obj:#w-> open the file for writing # b -> binary mode(objects,images,serialised data)
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)


#Evaluation of Models
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)


#For loading the pickle file, common functionality throughtout the entire project
def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    
    except Exception as e:
        raise CustomException(e,sys)
        

        