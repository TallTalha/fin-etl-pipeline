from datetime import datetime
import pandas as pd
from typing import Dict, Any
from utils.logger import setup_logger
import logging
import os

# Setup logger
logger = setup_logger('logs/transformations.log', logging.INFO)

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