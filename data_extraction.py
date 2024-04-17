import pandas as pd
from database_utils import DatabaseConnector
import tabula
import requests
import boto3


class DataExtractor:
    connector=DatabaseConnector()
    def __init__(self):

        pass 

    def read_rds_table(self,connector,table_name):
        table_name_list = connector.list_db_tables("db_creds.yaml")
        if table_name in table_name_list:
            engine = connector.init_db_engine("db_creds.yaml")
            query=f'Select * from {table_name}'
            with engine.connect() as connection:
                df = pd.read_sql(query, connection)
            
            return df
        else:
            return None
        

    def retrieve_pdf_data(self,pdf_link):
        
        df = tabula.read_pdf(pdf_link, pages="all", multiple_tables=True)
        concat_df= pd.concat(df,ignore_index=True)
        
        return concat_df

    def list_number_of_stores(self,endpoint,headers):
        
        response= requests.get(endpoint,headers=headers)
        number_of_stores=response.json()
        return number_of_stores
        
    
    
    
    def retrieve_stores_data(self,store_endpoint):
        store_data_list=[]
        headers={"x-api-key":"yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        for store_number in range(0,451):
            endpoint=store_endpoint.format(store_number=store_number)
            response=requests.get(endpoint,headers=headers)
            store_data=response.json()
            store_data_list.append(store_data)
        return pd.DataFrame(store_data_list)
    def extract_from_s3(self):
        #s3://data-handling-public/products.csv
        s3 = boto3.client('s3')
        s3.download_file('data-handling-public', 'products.csv', 'products.csv')    
        df = pd.read_csv('products.csv', index_col=0)
        return df
