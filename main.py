# main.py

from dotenv import load_dotenv
load_dotenv() # Before importing settings to ensure environment variables are loaded

from api.client import fetch_stock_data
from processing.transformations import process_api_data
from database.core import get_postgresql_engine
from processing.loader import load_price_data_to_postgres
from utils.logger import setup_logger
import config.settings as settings
import logging


def run_etl_pipeline():
    """
    Runs the ETL pipeline to extract stock data, transform it, and load it into PostgreSQL.
    """
    # Setup logger
    setup_logger()
    logger = logging.getLogger(__name__)
    logger.info("ETL pipeline started.")

    # Create PostgreSQL engine
    engine = get_postgresql_engine(
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            database=settings.DB_NAME
    )
    if not engine: # If engine creation fails, log the critical error and exit
        logger.critical("Database engine could not be created. Exiting application.")
        return
    
    # 1. Extract
    raw_data = fetch_stock_data(symbol=settings.API_SYMBOL,
                                interval=settings.API_INTERVAL,
                                function=settings.API_FUNCTION)
    
    # 2. Transform
    if raw_data:
        processed_df = process_api_data(raw_data)
        
        # 3. Load
        if not processed_df.empty:
            # Creates PostgreSQL engine

            # Loads the processed data into PostgreSQL
            load_price_data_to_postgres(
                engine=engine,
                prices_df=processed_df,
                symbol=settings.API_SYMBOL
            )


    
    logger.info("ETL pipeline finished.")

if __name__ == "__main__":
    run_etl_pipeline()