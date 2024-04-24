import pandas as pd
import re
import numpy as np
from dateutil import parser
class DataCleaning:
        
   def clean_user_data(self,user_data): 
          user_data.set_index('index',inplace=True)
          
          user_data.replace('NULL', np.nan, inplace=True)
          

          user_data= user_data.dropna(how='all')
         
          user_data['country_code'].replace({'GGB':'GB'} ,inplace=True)
          for index, code in user_data['country_code'].items():
         
               if len(code) > 3:
                    
                    user_data.drop(index, inplace=True)
          user_data.reset_index(drop=True)

          return user_data
   
   def clean_card_data(self,user_data):
        user_data.replace('NULL', np.nan, inplace=True)
        
        user_data=user_data.dropna(how='all')
        
        for index, card_number in user_data['card_number'].items():
               new_card_number = re.sub(r'[^0-9]', '', str(card_number))  
               user_data.loc[index, 'card_number'] = new_card_number
        
        user_data = user_data[user_data['expiry_date'].str.match(r'\d{2}/\d{2}')]
        
        
        for index,date in user_data['date_payment_confirmed'].items():
              pattern=r'\w+ \d{4} \d{2}'
              if re.match(pattern,date):
                    parts=date.split()
                    month= parts[0]
                    year=parts[1]
                    day=parts[2]
                    months={"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
                    month_num= months.get(month)
                    new_date=f'{year}-{month_num}-{day}'
                    user_data.loc[index,'date_payment_confirmed']=new_date
        
                    
        user_data.reset_index(drop=True,inplace=True)
        return user_data

       
   def called_clean_store_data(self,store_data):
          store_data.set_index('index',inplace=True)
          store_data.replace('NULL', np.nan, inplace=True)
          store_data=store_data.dropna(how='all')
          store_data.drop('lat', axis=1, inplace=True)
          store_data['continent'] = store_data['continent'].replace({'eeEurope': 'Europe', 'eeAmerica': 'America'})
          store_data = store_data[store_data['country_code'].str.len() < 3]
          store_data['opening_date']=store_data['opening_date'].str.replace('/','-')
          store_data['staff_numbers'] = store_data['staff_numbers'].str.replace(r'\D','',regex=True)

          store_data['opening_date'] = store_data['opening_date'].apply(lambda date: parser.parse(date).strftime('%Y-%m-%d'))

          store_data.replace('N/A', np.nan, inplace=True)
          
         
          store_data.reset_index(drop=True)
          
          return store_data

   
   def convert_product_weights(self, product_data):
        product_data = product_data.dropna(subset=['weight'])
        product_data['weight'] = product_data['weight'].str.replace(r'\W$','',regex=True)
        for index, weight in product_data['weight'].items():
               
               if 'x' in weight:  
                    quantity, unit = weight.split('x')
                    numeric_value = float(unit.replace('g', '')) / 1000  
                    converted_weight = float(quantity) * numeric_value
                    product_data.loc[index, 'weight'] = f"{converted_weight}kg"
               
               elif 'ml' in weight:
                    
                    numeric_value = float(weight.replace('ml', '')) / 1000  
                    product_data.loc[index, 'weight'] = f"{numeric_value}kg"

               elif 'oz' in weight:
                    
                    numeric_value = float(weight.replace('oz', '')) / 35.274  
                    product_data.loc[index, 'weight'] = f"{numeric_value}kg"
               
               elif 'g' in weight and 'kg' not in weight:  

                    numeric_value = float(weight.replace('g', '')) / 1000   
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
   
   def clean_dim_times(self,date_data):
          date_data.replace('NULL',np.nan, inplace=True)
          date_data=date_data.dropna(how='all')

          for index,day in date_data['day'].items():
                if len(day) > 2:
                      date_data.drop(index, inplace=True)
          for index,month in date_data['month'].items():
                if len(month) > 2:
                      date_data.drop(index, inplace=True)
     
          for index,year in date_data['year'].items():
                if len(year) > 4:
                      date_data.drop(index, inplace=True)

          
          date_data.reset_index()
          
          return date_data



     
     
        

