from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.pipelines.predict_pipeline import CustomData,PredictPipeline


application=Flask(__name__) # This basically gives the entry point where we need to execute

app = application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') # THis generally searches for the template folder

@app.route('/predictdata',methods=['GET','POST'])


# we will be calling the custom data, created in predict_pipeline
def predict_datapoint():
    '''
    Predicting the Datapoint, form action in HTML will trigger it 
    '''
    if request.method=='GET':
        return render_template('home.html')# Input data fields will be present
    else:
        #for POST - Own custom class, this will be created in predict pipeline too
        data=CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))

        )
        pred_df=data.get_data_as_data_frame()
        print(pred_df)
        print("Before Prediction")

        predict_pipeline=PredictPipeline()
        print("Mid Prediction")
        results=predict_pipeline.predict(pred_df)
        print("after Prediction")
        return render_template('home.html',results=results[0])#Output will be in the list format
    

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)   