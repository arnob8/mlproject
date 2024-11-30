#Will have common functionalities

import os
import sys


import numpy as np 
import pandas as pd 

from src.exception import CustomException

import dill

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