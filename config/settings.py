import os
from dotenv import load_dotenv

# Loasd environment variables from .env file
load_dotenv()

# API Parameters

## Basic API Configuration
API_SYMBOL = os.getenv("ALPHAVANTAGE_API_SYMBOL", "MSFT")
API_INTERVAL = os.getenv("ALPHAVANTAGE_API_INTERVAL", "1min")
API_FUNCTION = os.getenv("ALPHAVANTAGE_API_FUNCTION", "TIME_SERIES_INTRADAY")
API_OUTPUTSIZE = os.getenv("ALPHAVANTAGE_API_OUTPUTSIZE", "compact")
## Advanced API Configuration
API_OUTPUTFORMAT = os.getenv("ALPHAVANTAGE_API_OUTPUTFORMAT", "json")
API_DATATYPE = os.getenv("ALPHAVANTAGE_API_DATATYPE", "csv")
API_ADJUSTED = os.getenv("ALPHAVANTAGE_API_ADJUSTED", "false")
API_TIMEZONE = os.getenv("ALPHAVANTAGE_API_TIMEZONE", "US/Eastern")
API_DATETIMEFORMAT = os.getenv("ALPHAVANTAGE_API_DATETIMEFORMAT", "iso8601")


# Postgresql DB Configuration
DB_USER = os.getenv("POSTGRES_USER", "default_user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)
DB_NAME = os.getenv("POSTGRES_DB", "default_db")
DB_URL = os.getenv("POSTGRES_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# API Configuration
API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
BASE_URL = os.getenv("ALPHAVANTAGE_API_URL", "https://www.alphavantage.co/query")
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", 3))
API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", 5))
API_RATE_LIMIT_DAILY = int(os.getenv("API_RATE_LIMIT_DAILY", 25))  #  per day