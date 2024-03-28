import yaml
from database_utils import DatabaseConnector 
from data_extraction import DataExtractor  
from data_cleaning import DataCleaning 
import pandas as pd

connector = DatabaseConnector()
extractor = DataExtractor()
cleaner = DataCleaning()
table_name="legacy_users"
source_data = extractor.read_rds_table(connector, table_name)


cleaned_data = cleaner.clean_user_data(source_data)

cleaned_data.to_csv("legacy_users.csv", index= False)