import pandas as pd

class DataCleaning:
        
   def clean_user_data(self,user_data): 
        #Dropping NULL values first
        user_data= user_data.dropna()


        #Dropping wrong date like columns 
        date_columns= user_data.select_dtypes(include='datetime').columns
        user_data[date_columns]= user_data[date_columns].apply(pd.to_datetime, errors='coerce')
        user_data= user_data.dropna(subset=date_columns)

        #Dropping wrong numeric columns 
        numeric_columns=user_data.select_dtypes(include=['int','float']).columns
        user_data[numeric_columns]=user_data[numeric_columns].apply(pd.to_numeric, errors='coerce')
        user_data=user_data.dropna(subset=numeric_columns)

        return user_data
   