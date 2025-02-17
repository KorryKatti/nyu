import json
import requests
import yfinance as yf
import threading
import os
from index import get_headlines

# Load feed links from JSON file
def load_feed_links(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data["feed_links"]

# Fetch headlines using the loaded feed links
feed_links = load_feed_links('feed_links.json')

# Store headlines in a JSON file
headlines = get_headlines(feed_links)
with open('headlines.json', 'w') as f:
    json.dump(headlines, f)

# Stock data fetch functions
def get_30d_data(stock_name, api_key):
    """Fetch 30-day intraday stock data."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_name}&interval=5min&outputsize=full&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    with open(f'{stock_name}_month_data.json', 'w') as f:
        json.dump(data, f)

def get_5min_data(stock_name, api_key):
    """Fetch past 5-minute stock data."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_name}&interval=5min&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    with open(f'{stock_name}_minute_data.json', 'w') as f:
        json.dump(data, f)

def get_full_history(stock_name):
    """Fetch full historical data using yfinance."""
    stock = yf.Ticker(stock_name)
    stock_info = stock.history(period="max")
    stock_info.to_json(f'{stock_name}_stock_info.json')

# Run threads
def get_stock_data(stock_name, api_key):
    t1 = threading.Thread(target=get_30d_data, args=(stock_name, api_key))
    t2 = threading.Thread(target=get_5min_data, args=(stock_name, api_key))
    t3 = threading.Thread(target=get_full_history, args=(stock_name,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

# Example usage
api_key = os.getenv("alpha_api")
stock_name = "AAPL"
get_stock_data(stock_name, api_key)
print("All done")
