import yaml
from database_utils import DatabaseConnector 
from data_extraction import DataExtractor  
from data_cleaning import DataCleaning 
import pandas as pd
import tabula
import jpype
import requests

connector = DatabaseConnector()
extractor = DataExtractor()
cleaner = DataCleaning()
table_name="legacy_users"
source_data = extractor.read_rds_table(connector, table_name)


cleaned_data = cleaner.clean_user_data(source_data)
connector.upload_to_db(cleaned_data,"dim_users")
pdf_link='https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'

card= extractor.retrieve_pdf_data(pdf_link)
clean_card= cleaner.clean_card_data(card)
new_table_name='dim_card_details'
connector.upload_to_db(clean_card,new_table_name)





endpoint_number_stores='https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores'
headers={"x-api-key":"yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"}
        
list_number_of_stores=extractor.list_number_of_stores(endpoint_number_stores,headers)

print(list_number_of_stores)
store_url= "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{store_number}"
store_data=extractor.retrieve_stores_data(store_url)
clean_store_data=cleaner.called_clean_store_data(store_data)
print(clean_store_data.head(200))

connector.upload_to_db(clean_store_data,'dim_store_details')


products_df = extractor.extract_from_s3()
clean_products_df= cleaner.clean_product_data(product_data=products_df)
connector.upload_to_db(clean_products_df,'dim_products')
list_tables=connector.list_db_tables('db_creds.yaml')
orders_df=extractor.read_rds_table(connector,'orders_table')

clean_orders_data=cleaner.clean_orders_data(orders_df)
connector.upload_to_db(clean_orders_data,'orders_table')
list_tables=connector.list_db_tables('db_creds.yaml')
orders_df=extractor.read_rds_table(connector,'orders_table')

clean_orders_data=cleaner.clean_orders_data(orders_df)
connector.upload_to_db(clean_orders_data,'orders_table')

date_detail_url= 'https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'
response= requests.get(date_detail_url)

json_file=response.json()

date_times_df=pd.DataFrame(json_file)



connector.upload_to_db(date_times_df,'dim_date_times')
