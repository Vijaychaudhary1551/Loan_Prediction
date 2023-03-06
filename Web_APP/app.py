import os
import sys

# configuring the environment
os.environ["SPARK_HOME"] = "/home/talentum/spark/spark-3.3.2-bin-hadoop3"
os.environ["PYLIB"] = os.environ["SPARK_HOME"] + "/python/lib"
os.environ["PYSPARK_PYTHON"] = "/usr/bin/python3.6" 
os.environ["PYSPARK_DRIVER_PYTHON"] = "/usr/bin/python3"
sys.path.insert(0, os.environ["PYLIB"] +"/py4j-0.10.7-src.zip")
sys.path.insert(0, os.environ["PYLIB"] +"/pyspark.zip")
import pyspark

from flask import Flask, render_template, request
from pyspark.ml import PipelineModel
from Fetch import Fetch
from pyspark.sql.functions import *
from pyspark.sql import functions

app = Flask(__name__)

def preprocess(df):
# getting the numerical columns
    cat_columns = []
    num_columns = ['amnt','hour','days_before','weekofyear','hour_diff']
    for column in df.columns:
        if column not in num_columns:
            cat_columns.append(column)

    cat_columns.remove('app_id')
    # cat_columns.remove('transaction_number')
    # cat_columns.remove('__index_level_0__')
    # creating a new dataframe
    new_df = df.select('app_id').distinct()

    # handling the categorical columns
    for column in cat_columns:
        # grouping by app_id and categorical column & counting the occurences 
        cnts = df.groupby('app_id',column).count()
        
        # extracting the maximum count and its app_id 
        max_cnt = cnts.groupby('app_id').agg(max('count').alias('count'))
        
        # extracting the frequently occuring value
        mode = cnts.join(max_cnt,['app_id','count'],'inner')\
        .select('app_id',column)\
        .withColumnRenamed(column,'mode_'+column)
        
        # appending the newly created column to the original dataframe
        new_df = new_df.join(mode,'app_id','inner')
        
    # handling numerical columns
    for column in num_columns:
        # calculating the average of the numerical features
        avgs = df.groupby('app_id').agg(mean(column).alias('avg_'+column))
        
        # appending the column to the dataframe
        new_df = new_df.join(avgs,'app_id','inner')
    # returning the preprocessed dataframe
    return new_df

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/',methods = ['POST'])
def predict():
    fetch = Fetch('transactions')
    values = [str(val) for val in request.form.values()]
    try:
        # fetching the data from HBase
        df = fetch.get(values[0])
        # processing the data
        df = preprocess(df)
        # adding the entered product_id to the dataframe
        df = df.withColumn('product',functions.lit(int(values[1])))
        # loading the model
        model = PipelineModel.load('file:///home/talentum/test-jupyter/project-2/Web_APP/model')
        # making the prediction
        pred = model.transform(df)
        result = pred.select('prediction')\
            .take(1)[0]\
            .__getitem__('prediction')
    finally:
        fetch.close()
    

    if int(result) == 0:
        return render_template('indexnew.html',result = 'Sorry You are Not Eligible!')
    else:
        return render_template('indexnew.html',result = 'Congratulations!! You are Eligible.')  
    
# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	# app.run('127.0.0.0',port=8767)
    app.run('0.0.0.0',port=8767)
