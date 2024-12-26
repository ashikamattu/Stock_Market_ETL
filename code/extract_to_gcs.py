import requests
import csv
import pandas as pd
#from google.cloud import storage

tickers_df = pd.read_csv('./tickers.csv', dtype={'Symbol': str})
tickers_df['Symbol'] = tickers_df['Symbol'].str.strip()

url = 'https://yahoo-finance166.p.rapidapi.com/api/stock/get-financial-data'

headers = {
	"x-rapidapi-key": "6fe0cabaefmsh7ef3e2799f96313p13bba4jsn8315bbcfaddb",
	"x-rapidapi-host": "yahoo-finance166.p.rapidapi.com"
}
i = 0

field_names = ['ticker','currentPrice','totalRevenue','ebitda','freeCashflow','profitMargins','revenueGrowth','debtToEquity','totalDebt','numberOfAnalystOpinions','recommendationKey','timeStamp']
stocks_info_df = pd.DataFrame(columns = field_names)

for ticker in tickers_df['Symbol']:
    # For dev purpose only
    if (i == 3):
        break
    querystring = {"region":"US","symbol":ticker}
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json().get('quoteSummary', []).get('result',[])
        stock_info_dict = {}
        stock_info_dict['ticker'] = ticker
        # stock_info_dict['timestamp'] = timestamp 
        for entry in data[0]['financialData']:
            if ((entry in stocks_info_df.columns) and entry != 'recommendationKey'):
                stock_info_dict[entry] = data[0]['financialData'][entry]['raw']
            if ((entry in stocks_info_df.columns) and entry == 'recommendationKey'):
                stock_info_dict[entry] = data[0]['financialData'][entry]
        stocks_info_df = pd.concat([stocks_info_df,pd.DataFrame([stock_info_dict])], ignore_index = True)

    else:
        print("Failed to fetch data:", response.status_code)

    i += 1
# Validate and Upload stocks_info_df to CSV file

# Upload the CSV file to GCS
'''
bucket_name = 'bkt-stocks'
#storage_client = storage.Client()
#bucket = storage_client.bucket(bucket_name)
destination_blob_name = f'{csv_filename}'  # The path to store in GCS

blob = bucket.blob(destination_blob_name)
blob.upload_from_filename(csv_filename)

print(f"File {csv_filename} uploaded to GCS bucket {bucket_name} as {destination_blob_name}")
'''