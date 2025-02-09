import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object # to load our pickle file

#First Class -> has the init function without nothing, 
class PredictPipeline:
    def __init__(self):
        pass

    #will simply do prediction
    # two pckle files we have currently, preprocessor and  model
    def predict(self,features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'
            #load_obect we will craete, will load the pickle file
            model = load_object(file_path = model_path) #should be created in utils
            preprocessor = load_object(file_path = preprocessor_path)
            #print("Exploring the preprocessor object")
            #print(type(preprocessor))
            #print(preprocessor.transformers)
            data_scaled = preprocessor.transform(features)
            print("Exploring the model object")
            print(type(model))
            preds = model.predict(data_scaled)
            return preds

        except Exception as e:
            raise CustomException(e,sys)
        


#Second Class -> Responsible for matching all the input we are passing in the html to the backend
class CustomData:
    def __init__( self,           
            gender: str,
            race_ethnicity: str,
            parental_level_of_education,
            lunch: str,
            test_preparation_course: str,
            reading_score: int,
            writing_score: int):

            #Creating variable using self, the values are coming from web app agianst the respective variable
            self.gender = gender
            self.race_ethnicity = race_ethnicity
            self.parental_level_of_education = parental_level_of_education
            self.lunch = lunch
            self.test_preparation_course = test_preparation_course
            self.reading_score = reading_score
            self.writing_score = writing_score

    #It will basically return all our input in the form of a dataframe
    #From my web appplication , will get mapped to a datafram
    #could have been done in app.py but due to modularisation it is showed here 
    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education":[self.parental_level_of_education],
                "lunch":[self.lunch],
                "test_preparation_course":[self.test_preparation_course],
                "reading_score":[self.reading_score],
                "writing_score":[self.writing_score]

            }
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e,sys)