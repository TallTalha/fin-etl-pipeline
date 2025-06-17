#api_script.py
# This script is used to fetch data from an API and save it to a CSV file.

# import necessary libraries
import os # Proviedes funcitons for operating system process
import time # Provides time-related function
import requests # Provides functions for making HTTP requests
import logging # Provides functions for logging 
from typing import Optional # Provides support for type hints
from datetime import datetime # Provides functions for manipulating dates and times
import pandas as pd # Provides data manipulation and analysis tools

# Loads environment variables from a .env file
from dotenv import load_dotenv 
# Loads environment variables from a .env file
load_dotenv() 

# Imports the setup_logger function from log_config.py
from log_config import setup_logger 
# Sets up the logger
logger = setup_logger('logs/api_script.log', logging.INFO)

# API Information
API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')  # Fetches the API key from .env file
API_URL = 'https://www.alphavantage.co/query'  # Base URL for the API

# Retry configuration
MAX_RETIRES = 3 # Maximum number of retries for API requests
RETRY_DELAY = 5 # Delay in seconds before retrying a failed request
MAX_REQUESTS_PER_DAY = 25 # Maximum number of requests allowed per day

def fetch_stock_data(
        symbol: str = 'MSFT',
        interval: str = '1min',
        function: str = 'TIME_SERIES_INTRADAY'
) -> Optional[pd.DataFrame]:
    """
    Fetches data from the Alpha Vantage API.

    :param symbol: The stock symbol to fetch data for (default is 'MSFT').
    :param interval: The time interval for the data (default is '1min').
    :param function: The function to call on the API (default is 'TIME_SERIES_INTRADAY').
    :return: A DataFrame containing the fetched data, or None if an error occurs.
    """
    params = {
        'functiom': function,
        'symbol' : symbol,
        'interval': interval,
        'apikey': API_KEY
    }

    for attempt in range(1, MAX_RETIRES+1):
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status() # Raises an HTTPError for bad responses and then "expect block" to be executed
            data = response.json() # Parses the JSON response
            
            if 'Time Series' not in str(data):
                if 'Error Message' in data:
                    # Logs an error message if the API returns an error
                    logger.error(f"api_script.py: Error fetching data for {symbol} -> {data['Error Message']}")
                elif 'Note' in data:
                    # Logs a warning if the API rate limit is exceeded
                    logger.warning(f"api_script.py: API call limit reached -> {data['Note']}")
                else:
                    # Logs an error if the response does not contain expected data
                    logger.error(f"api_script.py: Unexpected response format for {symbol} -> {data}")
                return None
            
            # Gets dynamic key for the time series data
            key = [k for k in data.json() if "Time Series" in k][0]
            
            # Converts the time series data to a DataFrame
            df = pd.DataFrame.from_dict(data[key], orient='index', dtype=float)
            df.index.name = 'timestamp'  # Sets the index name to 'timestamp'
            print(df.columns) # Debugging line to check the columns of the DataFrame
            
            df.index = pd.to_datetime(df.index)  # Converts the index to datetime
            df.sort_index(inplace=True)  # Sorts the DataFrame by index
            return df  # Returns the DataFrame
        except requests.exceptions.RequestException as e:
            logging.error(f"api_script.py: Request failed for {symbol} on attempt {attempt}: {e}")
            if attempt < MAX_RETIRES:
                logger.info(f"api_script.py: Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"api_script.py: Max retries reached for {symbol}. Giving up.")
                return None
    return None  # Returns None if all attempts fail


