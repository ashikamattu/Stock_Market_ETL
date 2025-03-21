import requests
import csv
import pandas as pd
from google.cloud import storage
import datetime;
from dotenv import load_dotenv
import os

load_dotenv()

# Create a .env file in the same directory as the code. Store the API_KEY and HOST in it.

url = "https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data"

api_key = os.getenv("API_KEY")
host = os.getenv("HOST")

headers = {
	"x-rapidapi-key": api_key,
	"x-rapidapi-host": host
}

tickers_df = pd.read_csv('./tickers.csv', dtype={'Symbol': str})
tickers_df['Symbol'] = tickers_df['Symbol'].str.strip()

field_names = ['ticker','currentPrice','totalRevenue','ebitda','freeCashflow','profitMargins','revenueGrowth','debtToEquity','totalDebt','numberOfAnalystOpinions','recommendationKey','timeStamp']
stocks_info_df = pd.DataFrame(columns = field_names)

for ticker in tickers_df['Symbol']:
    querystring = {"region":"US","symbol":ticker}
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json().get('quoteSummary', []).get('result',[])#.get('0',[]).get('financialData',[])
        stock_info_dict = {}
        stock_info_dict['ticker'] = ticker
        current_timestamp = datetime.datetime.now() 
        stock_info_dict['timeStamp'] = current_timestamp 
        for entry in data[0]['financialData']:
            if ((entry in stocks_info_df.columns) and entry != 'recommendationKey' and data[0]['financialData'][entry] != {}):
                stock_info_dict[entry] = data[0]['financialData'][entry]['raw']
            if ((entry in stocks_info_df.columns) and entry == 'recommendationKey'):
                stock_info_dict[entry] = data[0]['financialData'][entry]
        stocks_info_df = pd.concat([stocks_info_df,pd.DataFrame([stock_info_dict])], ignore_index = True)
    else:
        print("Failed to fetch data:", response.status_code)
        exit()

print("API Data fetched successfully.")

# Validate and Upload stocks_info_df to CSV file
current_timestamp = stocks_info_df['timeStamp'].max()
csv_filename = str('./data/daily_stock_data_' + str(current_timestamp).replace(":", "-") + '.csv')

stocks_info_df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")

# Upload the CSV file to GCS

bucket_name = 'bkt-stocks'
source_file_name = csv_filename 
destination_blob_name = str('daily_stock_data_' + str(current_timestamp).replace(":", "-") + '.csv' ) 

storage_client = storage.Client(project='noted-point-444318-r3')
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(source_file_name)

# TODO - Implement Logging system to log the success of the upload
print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

'''
TODO: Check if the file you are uploading already exists in the bucket. Or GCP might handle this already. Double check. 
blobs = storage_client.list_blobs(bucket_name)

for blob in blobs:
    print(blob.name)'''