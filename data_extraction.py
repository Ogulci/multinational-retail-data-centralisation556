import pandas as pd
from database_utils import DatabaseConnector

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
        

