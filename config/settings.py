import os
from dotenv import load_dotenv

# Loasd environment variables from .env file
load_dotenv()

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