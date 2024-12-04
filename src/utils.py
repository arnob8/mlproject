#Will have common functionalities

import os
import sys


import numpy as np 
import pandas as pd 

from src.exception import CustomException

import dill
from sklearn.metrics import r2_score

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
def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i] 
            #models.values => returns all the values(model objects) from the dict
            #list(models.values()) => converts these values into a list
            #list(models.values())[i] retrieves the model object at the i-th position.

            model.fit(X_train,y_train) # Train Modelon Training data

            #Predict for both Train and test
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            #Calculate R2 Score for Train and Test
            train_model_score = r2_score(y_train,y_train_pred)
            test_model_score = r2_score(y_test,y_test_pred)

            report[list(models.keys())[i]] = test_model_score
            #Explanation =>
            #report[key] = value: Adds an entry to the dictionary, where:
            #key is the model name (list(models.keys())[i]).
            #value is the model's test performance score (test_model_score)
        return report
        
    except Exception as e:
        raise CustomException(e,sys)

        