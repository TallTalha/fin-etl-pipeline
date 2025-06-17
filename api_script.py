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
            
        except
