# main.py

from api.client import fetch_stock_data
from processing.transformations import process_api_data
from database.core import save_to_postgres
from utils.logger import setup_logger

def run_etl_pipeline():
    logger = setup_logger()
    logger.info("ETL pipeline started.")
    
    # 1. Extract
    raw_data = fetch_stock_data(symbol='MSFT')
    
    # 2. Transform
    if raw_data:
        processed_df = process_api_data(raw_data)
        
        # 3. Load
        if not processed_df.empty:
            save_to_postgres(processed_df, 'stock_data_intraday', 'MSFT')
    
    logger.info("ETL pipeline finished.")

if __name__ == "__main__":
    run_etl_pipeline()