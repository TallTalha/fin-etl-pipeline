# database/core.py
from sqlalchemy import create_engine, text, types
from sqlalchemy.types import TypeEngine
import pandas as pd
from typing import Dict
import logging
from utils.logger import setup_logger

# Setup logger
logger = setup_logger('logs/database.log', logging.INFO)

# Setup column types for PostgreSQL
columns_type: Dict[str, TypeEngine] = { 
    'timestamp': types.TIMESTAMP(timezone=True),
    'open': types.NUMERIC(precision=10, scale=4),
    'high': types.NUMERIC(precision=10, scale=4),
    'low':  types.NUMERIC(precision=10, scale=4),
    'close': types.NUMERIC(precision=10, scale=4),
    'volume': types.BIGINT
}

def get_postgresql_engine(user, password, host, port, database):
    """
    Creates a SQLAlchemy engine for PostgreSQL database connection.

    Args:
        user: Database username
        password: Database password
        host: Database host
        port: Database port
        database: Database name

    Returns:
        SQLAlchemy engine object
    """
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    try:
        # Check if the connection string is valid
        engine = create_engine(connection_string)
        logger.info(f"PostgreSQL engine created with connection string: {connection_string}")
        return engine
    except Exception as e:
        logger.error(f"Error creating PostgreSQL engine: {e}")
        return None
    

def save_to_postgresql(engine, df: pd.DataFrame, table_name: str, columns_type: dict, symbol: str):
    """
    Saves a DataFrame to a PostgreSQL database table.

    Args:
        engine: SQLAlchemy engine object
        df: DataFrame to save
        table_name: Name of the table to save the DataFrame to
        columns_type: Dictionary mapping column names to their SQL data types ('name': 'type').

    Returns:
        None
    """
    try:
        logger.info(f"Writing '{len(df)}' rows to table '{table_name}' for symbol '{symbol}'...")
        
        df.to_sql(
            name=table_name,
            dtype=columns_type,
            con=engine,
            if_exists='append',

            index=True,
            index_label='timestamp'
        )
        logger.info(f"Data for '{symbol}' successfully saved to table '{table_name}'.")
    
        return True
    except Exception as e:
        logger.error(f"Error saving '{symbol}' DataFrame to table:'{table_name}'  -> Error: {e}")
        return False
        