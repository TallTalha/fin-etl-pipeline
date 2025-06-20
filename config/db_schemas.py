# config/db_schemas.py
from sqlalchemy import types
from sqlalchemy.types import TypeEngine
from typing import Dict

# fact_prices schema for stock data
# This schema already defined in the database, so we just define the dtypes here
FACT_PRICES_DTYPES: Dict[str, TypeEngine] = {
    'open': types.NUMERIC(precision=10, scale=4),
    'high': types.NUMERIC(precision=10, scale=4),
    'low': types.NUMERIC(precision=10, scale=4),
    'close': types.NUMERIC(precision=10, scale=4),
    'volume': types.BIGINT
}

# In future, i can define other schemas like this:
# DIM_STOCKS_DTYPES: Dict[str, TypeEngine] = {
#     'symbol': types.String(10),
#     'name': types.String(100),
#     'sector': types.String(50),
#     'industry': types.String(50),
#     'exchange': types.String(10)
# }
