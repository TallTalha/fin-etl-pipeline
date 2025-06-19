# database/core.py
from sqlalchemy import create_engine, text, types
from sqlalchemy.types import TypeEngine
from sqlalchemy.engine import Engine
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
    

def save_dataframe(engine: Engine,
                    df: pd.DataFrame,
                    table_name: str,
                    columns_type: dict,
                    if_exists: str = 'append',
                    index: bool = False,
                    index_label: str = None,
                    dtype: dict = None,
) -> bool:
    """
    Saves a DataFrame to a PostgreSQL database table.
    Args:
        engine: SQLAlchemy engine object.
        df: DataFrame to save.
        table_name: Name of the table to save the DataFrame.
        columns_type: Dictionary of column types for the DataFrame.
        if_exists: Behavior when the table already exists ('fail', 'replace', 'append'). Default is 'append'.
        index: Whether to write row names (index). Default is False.
        index_label: Column label for index column. Default is None.
        dtype: Dictionary of column types for the DataFrame. Default is None.
    Returns:
        True if successful, False otherwise.
    """
    try:
        logger.info(f"Writing {len(df)} rows to table '{table_name}'...")
        
        df.to_sql(
            name=table_name,
            dtype=dtype,
            con=engine,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
        )
        logger.info(f"Data successfully saved to table '{table_name}'.")
    
        return True
    except Exception as e:
        logger.error(f"Failed to save DataFrame to table '{table_name}'. Error: {e}")
        return False
        