import os
import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from log_config import setup_logger

# Configuration
load_dotenv()
logger = setup_logger('logs/api_script.log', logging.INFO)

class APIConfig:
    BASE_URL = 'https://www.alphavantage.co/query'
    KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    MAX_RETRIES = 3  # maximum number of retries for API requests
    RETRY_DELAY = 5  # seconds
    RATE_LIMIT = 25  # requests per day

def fetch_stock_data(
    symbol: str = 'MSFT',
    interval: str = '1min',
    function: str = 'TIME_SERIES_INTRADAY'
) -> Optional[pd.DataFrame]: 
    """
    Fetches stock data from Alpha Vantage API.
    
    Args:
        symbol: Stock ticker symbol
        interval: Time interval between data points
        function: API function to call
        
    Returns:
        DataFrame with stock data or None if failed
    """
    params = {
        'function': function,
        'symbol': symbol,
        'interval': interval,
        'apikey': APIConfig.KEY
    }

    for attempt in range(1, APIConfig.MAX_RETRIES + 1):
        try:
            response = requests.get(APIConfig.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Find time series key dynamically
            time_series_key = next((k for k in data if "Time Series" in k), None)
            
            if not time_series_key:
                handle_api_errors(data, symbol)
                return None

            df = process_api_data(data[time_series_key])
            return df

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed (attempt {attempt}): {str(e)}")
            if attempt < APIConfig.MAX_RETRIES:
                time.sleep(APIConfig.RETRY_DELAY)
    
    logger.error(f"Max retries reached for {symbol}")
    return None

def handle_api_errors(data: Dict[str, Any], symbol: str) -> None:
    """Handles different types of API error responses."""
    if 'Error Message' in data:
        logger.error(f"API error for {symbol}: {data['Error Message']}")
    elif 'Note' in data:
        logger.warning(f"Rate limit exceeded: {data['Note']}")
    else:
        logger.error(f"Unexpected response format for {symbol}: {data}")

def process_api_data(time_series_data: Dict[str, Any]) -> pd.DataFrame:
    """Converts API time series data to DataFrame and cleans it."""
    df = pd.DataFrame.from_dict(time_series_data, orient='index', dtype=float)
    df.index = pd.to_datetime(df.index)
    df.index.name = 'timestamp'
    df.sort_index(inplace=True)
    
    # Clean column names (remove prefixes like '1. ')
    df.columns = [col.split('. ')[-1] for col in df.columns]
    
    return df

def save_to_csv(df: pd.DataFrame, symbol: str) -> None:
    """
    Saves DataFrame to CSV file.
    
    Args:
        df: DataFrame to save
        symbol: Stock ticker symbol for the filename
    """
    if df.empty:
        logger.warning(f"No data to save for {symbol}. DataFrame is empty.")
    else:
        today = datetime.now().strftime('%Y-%m-%d')
        os.makedirs('data', exist_ok=True)
        file_path = f'data/{symbol}_{today}.csv'
        df.to_csv(file_path)
        logger.info(f"Data saved to {file_path}")
        print(df.head())  # Display first few rows of the DataFrame

if __name__ == "__main__":
    # Example usage
    stock_symbol = 'MSFT'
    interval = '15min' # The following values are supported: 1min, 5min, 15min, 30min, 60min
    function = 'TIME_SERIES_INTRADAY'
    stock_data = fetch_stock_data(symbol=stock_symbol, interval=interval, function=function)
    
    if stock_data is not None:
        save_to_csv(stock_data, stock_symbol)
    else:
        logger.error(f"Failed to fetch data for {stock_symbol}.")
#return None
