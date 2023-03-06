import os
import sys
import happybase
import pyspark
from pyspark.sql.types import *
# from pyspark.sql import functions

class Fetch:
    def __init__(self,table_name):
        # creating sparksessio and connection to HBase Table
        self.spark = pyspark.sql.SparkSession\
                .builder\
                .appName("toDataframe")\
                .getOrCreate()
        # connection with HBase and HBase table
        self.connection = happybase.Connection(host='localhost',protocol='compact')
        self.table = self.connection.table(table_name)
    
    def _process(self,row_key,region):
        """
        This method processes each region of HBase and returns a dicionary 
        of the data present in the region.
        """
        processed = dict()
        row_key = row_key.decode('utf-8').strip('_[0-9]{6}')
        processed.update({'app_id':int(row_key)})
        for key,value in region.items():
            # converting byte data in string
            key = key.decode('utf-8')[8:len(key)]
            value = value.decode('utf-8')
            # if the column is amnt convert it into float else convert to int
            if key == 'amnt':
                value = float(value)
            else:
                value = int(value)
            # updating the dictionary
            pair = {key:value}
            processed.update(pair)
        # returning the processed data
        return processed
    
    def _convertToDF(self,df):
        """
        This method converts list of records in spark dataframe.
        """
        schema = StructType([
        StructField('app_id', IntegerType() , False),
        StructField('amnt', DoubleType() , True),
        StructField('currency', IntegerType() , True),
        StructField('operation_kind', IntegerType() , True),
        StructField('card_type', IntegerType() , True),
        StructField('operation_type', IntegerType() , True),
        StructField('operation_type_group', IntegerType() , True),
        StructField('ecommerce_flag', IntegerType() , True),
        StructField('payment_system', IntegerType() , True),
        StructField('income_flag', IntegerType() , True),
        StructField('mcc', IntegerType() , True),
        StructField('country', IntegerType() , True),
        StructField('city', IntegerType() , True),
        StructField('mcc_category', IntegerType() , True),
        StructField('day_of_week', IntegerType() , True),
        StructField('hour', IntegerType() , True),
        StructField('days_before', IntegerType() , True),
        StructField('weekofyear', IntegerType() , True),
        StructField('hour_diff', LongType() , True),
        StructField('__index_level_0__', LongType() , True)
        ])
        return self.spark.createDataFrame(df,schema=schema)
    
    def get(self,customer_id):
        """
        This method retrieves the data from HBase, processes it and converts it 
        into spark dataframe
        """
        # converting the customer id for accurate output using row_prefix
        customer_id = bytes(customer_id + '_',encoding='utf-8')
        df = []
        # fething all the records matching the customer id from the table
        for row_key,region in self.table.scan(row_prefix=customer_id):
            # process and append to the list
            data = self._process(row_key,region)
            df.append(data)
        # returning the dataframe
        return self._convertToDF(df)

    def close(self):
        """
        Method for closing resources.
        """
        self.connection.close()
        self.spark.stop()