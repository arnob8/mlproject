import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_models

@dataclass
class ModelTrainerConfig: 
    #This ModelTrainerConfig class holds a configuration for the model trainer.
    #after creating model ,will want to save my pickle file
    trained_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    #Step 1 -Main Class uses the configuration defined in ModelTrainerConfig to train and save
    #the models

    #Step 2 - #the __init__ method initialises the model_trainer_config attribute
        #with an instance of ModelTrainerConfig
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig() 
        
        #THis provides access to config details(like the filepath for saving the model) via
        #self.model_trainer_config
        #basically inside the variable we will get the path name

    #Step 3 - Divides the train and test array into predictor and target variables
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Split training and test input data")
            X_train,y_train,X_test,y_test=(
                train_array[:,:-1], #store all columns except the last one(target) in X_train
                train_array[:,-1], #stores only the target variable
                test_array[:,:-1],
                test_array[:,-1]
            )
    
    #Step 4 - Create dict of models
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                #"K-Neighbors Classifier": KNeighborsRegressor(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose = False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }

    #Step 4.5 - Adding Parameters as part of video series 272 - For Model Hyperparameter tuning

            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regression":{},
                "XGBRegressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
    #Step 5 - Dictionary to store all the model results
            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models = models
            ,param = params)
    
    #Step 6 - To get the best model score from dictionary
            best_model_score = max(sorted(model_report.values()))

    #Step 7 - To get the best model name from dictionary
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

    #Step 8 - Selecting best model
            best_model = models[best_model_name]

    #Step 9 - Raising Custom Exception

            if best_model_score<0.6:
                raise CustomException("No best model found")

            logging.info(f"Best found model on both training and testing dataset")

 #Step 10 - Save the model part - basically dumping the best model

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

    #Step 11 - Check predicted output for the test data
            predicted = best_model.predict(X_test)

            #Check R2 Score
            r2_square = r2_score(y_test,predicted)
            return r2_square
            
        except Exception as e:
            raise CustomException(e,sys)


 