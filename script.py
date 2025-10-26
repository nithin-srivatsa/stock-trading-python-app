import requests
import os
from dotenv import load_dotenv
import time
import csv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
response = requests.get(url)
tickers = []
data = response.json()
for ticker in data['results']:
    tickers.append(ticker)

while 'next_url' in data:
    print("fetching next page", data['next_url'])
    time.sleep(12)
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    for ticker in data['results']:
        tickers.append(ticker)

print("ticker count:", len(tickers))

example_schema = {'ticker': 'HP', 
'name': 'Helmerich & Payne, Inc.', 
'market': 'stocks', 
'locale': 'us', 
'primary_exchange': 'XNYS', 
'type': 'CS', 
'active': True, 
'currency_name': 'usd', 
'cik': '0000046765', 
'composite_figi': 'BBG000BLCPY4', 
'share_class_figi': 'BBG001S5RZP1', 
'last_updated_utc': '2025-10-26T06:05:40.686309715Z'}

# Write tickers to CSV file using example_schema structure
csv_filename = 'tickers.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(example_schema.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for ticker in tickers:
        writer.writerow(ticker)

print(f"Results written to {csv_filename}")