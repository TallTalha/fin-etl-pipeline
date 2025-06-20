import os
import time
import logging
from config.settings import API_KEY, BASE_URL
from typing import Optional, Dict, Any

import requests


# Setup logger
logger = logging.getLogger(__name__) 

class APIConfig:
    BASE_URL = BASE_URL or 'https://www.alphavantage.co/query'
    KEY = API_KEY 
    MAX_RETRIES = 3  # maximum number of retries for API requests
    RETRY_DELAY = 5  # seconds
    RATE_LIMIT = 25  # requests per day

def fetch_stock_data(
    symbol: str = 'MSFT',
    interval: str = '1min',
    function: str = 'TIME_SERIES_INTRADAY'
) -> Optional[Dict[str, Any]]: 
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

    logger.info(f"API request started for symbol: {symbol} (function: {function}, interval: {interval})")
    for attempt in range(1, APIConfig.MAX_RETRIES + 1):
        logger.info(f"Attempt {attempt}/{APIConfig.MAX_RETRIES} for symbol {symbol}")
        try:
            response = requests.get(APIConfig.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            # Find time series key dynamically
            time_series_key = next((k for k in data if "Time Series" in k), None)
            
            if not time_series_key:
                handle_api_errors(data, symbol)
                return None

            logger.info(f"API response received for {symbol}. API request successful.")
            return data[time_series_key]

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

