import json
import yfinance as yf
import threading
import os
from index import get_headlines
from tvDatafeed import TvDatafeed, Interval

# load feed links from JSON file
def load_feed_links(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data["feed_links"]

# fetch headlines using the loaded feed links
feed_links = load_feed_links('feed_links.json')

tv = TvDatafeed()

# store headlines in a JSON file
headlines = get_headlines(feed_links)
with open('headlines.json', 'w') as f:
    json.dump(headlines, f)

# stock data fetch functions

import json
from tvDatafeed import TvDatafeed, Interval

def get_30d_data(stock_name):
    """Fetch 30-day intraday stock data using tvDatafeed."""
    # Initialize TvDatafeed instance
    tv = TvDatafeed()
    
    # Set the interval to 2 hours
    interval = Interval.in_2_hour  # 2-hour interval
    
    # Calculate the number of bars needed (30 days)
    n_bars = 30
    
    # Fetch historical data
    data = tv.get_hist(symbol=stock_name, exchange='NASDAQ', interval=interval, n_bars=n_bars)
    
    if data is not None:
        # Convert timestamps to strings for JSON compatibility
        data.index = data.index.strftime('%Y-%m-%d %H:%M:%S')
        # Convert DataFrame to dictionary and write to file
        with open(f'{stock_name}_30d_data.json', 'w') as f:
            json.dump(data.to_dict(), f)  # Convert DataFrame to dict before dumping
    else:
        print(f"Error fetching data for {stock_name}.")



def get_5min_data(stock_name):
    """fetch recent 5-minute stock data using tvDatafeed"""
    # fetching one day's worth of 5-min bars (~78 bars)
    n_bars = 78
    data = tv.get_hist(symbol=stock_name, exchange='NASDAQ', interval=Interval.in_5_minute, n_bars=n_bars)
    
    if data is not None:
        # Convert timestamps to strings for JSON compatibility
        data.index = data.index.strftime('%Y-%m-%d %H:%M:%S')
        # Convert DataFrame to dictionary and write to file
        with open(f'{stock_name}_minute_data.json', 'w') as f:
            json.dump(data.to_dict(), f)  # Convert DataFrame to dict before dumping
    else:
        print(f"Error fetching data for {stock_name}.")


def get_full_history(stock_name):
    """fetch full historical data using yfinance"""
    stock = yf.Ticker(stock_name)
    stock_info = stock.history(period="max")
    stock_info.to_json(f'{stock_name}_stock_info.json')

# run threads
def get_stock_data(stock_name):
    t1 = threading.Thread(target=get_30d_data, args=(stock_name,))
    t2 = threading.Thread(target=get_5min_data, args=(stock_name,))
    t3 = threading.Thread(target=get_full_history, args=(stock_name,))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

def trigger_stock_data_retrieval(stock_name):
    print(f"Fetching data for {stock_name}...")
    get_stock_data(stock_name)
    print(f"Data retrieval for {stock_name} complete!")

# Example trigger
stock_name = "AAPL"  # Replace with any stock ticker
trigger_stock_data_retrieval(stock_name)
