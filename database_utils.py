import pandas as pd
import yaml
import sqlalchemy
from sqlalchemy import text
class  DatabaseConnector: 
    def __init__(self):
        pass


    def read_db_creds(self,data):
        
        with open(data,'r') as yaml_data:
            
            credentials=yaml.safe_load(yaml_data)
        return credentials
        

    def init_db_engine(self,data):
        credentials=self.read_db_creds(data)
        engine=sqlalchemy.create_engine(f"postgresql://{credentials['RDS_USER']}:{credentials['RDS_PASSWORD']}@{credentials['RDS_HOST']}:{credentials['RDS_PORT']}/{credentials['RDS_DATABASE']}")
        return engine
    
    
    def list_db_tables(self,data):
        engine=self.init_db_engine(data)
        with engine.connect() as connection:
             query = text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
             result = connection.execute(query)
             table_names = [row[0] for row in result]
        return table_names
    
    def upload_to_db(self, df, table_name):
        engine=self.init_db_engine('new_creds.yaml')
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    
