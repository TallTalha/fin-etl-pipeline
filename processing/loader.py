from sqlalchemy.engine import Engine
from database.core import get_or_create_stock_id
import pandas as pd
import logging
from config.db_schemas import FACT_PRICES_DTYPES

# Setup logger
logger = logging.getLogger(__name__) 

def load_price_data_to_postgres(
        engine: Engine,
        prices_df: pd.DataFrame,
        symbol: str
        ) -> bool:
    """
    Loads price data into PostgreSQL database.
    Args:
        engine: SQLAlchemy engine object.
        df: DataFrame containing price data.
        symbol: Stock ticker symbol for the data.
    Returns:
        True if data is loaded successfully, False otherwise.
    """
    try:
        with engine.begin() as connection: #Transaction begins here
            logger.info(f"Starting transaction for {symbol}...")

            # Stock ID retrieval or creation
            stock_id = get_or_create_stock_id(connection=connection, symbol=symbol)

            # Prepare DataFrame for insertion
            fact_df = prices_df.copy()
            fact_df['stock_id'] = stock_id

            #Connect to the database and write the DataFrame
            fact_df.to_sql(
                name='fact_prices',
                con=connection,
                if_exists='append',
                index=True,
                index_label='timestamp',
                dtype=FACT_PRICES_DTYPES
            )
        logger.info(f"Transaction for {symbol} committed successfully.")
        return True
    except Exception as e:
        logger.error(f"Transaction for {symbol} failed and was rolled back. Error: {e}")
        return False


