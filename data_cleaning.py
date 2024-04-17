import pandas as pd
import re

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
   
   def clean_card_data(self,user_data):

        user_data=user_data.dropna(how='all')
        user_data=user_data.drop_duplicates()


        user_data['card_number'] = pd.to_numeric(user_data['card_number'], errors='coerce')
        user_data=user_data.dropna(subset=['card_number'])
        

        user_data['date_payment_confirmed']=pd.to_datetime(user_data['date_payment_confirmed'], format='%Y-%m-%d', errors='coerce')
        user_data=user_data.dropna(subset=['date_payment_confirmed'])
        
        return user_data

       
   def called_clean_store_data(self,store_data):
          store_data.set_index('index',inplace=True)
          store_data=store_data.dropna(how='all')
          store_data.drop('lat', axis=1, inplace=True)
          store_data['continent'] = store_data['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
          store_data =store_data[store_data['address'] != 'N/A']

          store_data['opening_date']=store_data['opening_date'].apply(pd.to_datetime,errors='coerce')
          
          store_data=store_data.dropna(subset=['opening_date'])
          store_data.reset_index(drop=True)
          return store_data

   
   def convert_product_weights(self, product_data):
        product_data = product_data.dropna(subset=['weight'])
        
        for index, weight in product_data['weight'].items():
               
               if 'x' in weight:  
                    quantity, unit = weight.split('x')
                    numeric_value = float(unit.replace('g', '')) / 1000  
                    converted_weight = float(quantity) * numeric_value
                    product_data.loc[index, 'weight'] = f"{converted_weight}kg"
               
               elif 'ml' in weight:
                    
                    numeric_value = float(weight.replace('ml', '')) / 1000  
                    product_data.loc[index, 'weight'] = f"{numeric_value}kg"
               
               elif weight[-1] == 'g' and weight[-2:] !='kg':  

                    numeric_value = float(weight[:-1]) / 1000 
                    product_data.loc[index, 'weight'] = f"{numeric_value}kg"
            
               else:
                    product_data.loc[index, 'weight'] = weight
            

        return product_data

   def clean_product_data(self,product_data):
          
          data=self.convert_product_weights(product_data)
          clean_df= data.drop_duplicates()
          
          clean_df['date_added']=clean_df['date_added'].apply(pd.to_datetime, errors='coerce')
          
          clean_df=clean_df.dropna(subset='date_added')
          
          return clean_df
   def clean_orders_data (self,orders_data):
        
        orders_data.set_index('index', inplace=True)

        orders_data.drop(columns=['first_name','last_name','1','level_0'], inplace=True)
        
        return orders_data


     
     
        

