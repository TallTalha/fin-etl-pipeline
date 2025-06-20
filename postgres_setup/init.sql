-- This script initializes the PostgreSQL database schema for a stock market data warehouse.
CREATE TABLE dim_stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(16) NOT NULL UNIQUE,
    company_name VARCHAR(255),
    sector VARCHAR(100),
    country VARCHAR(100),
    market_cap BIGINT,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE fact_prices (
    stock_id INT NOT NULL,
    "timestamp" TIMESTAMPTZ NOT NULL,
    "open" NUMERIC(10, 4),
    high NUMERIC(10, 4),
    low NUMERIC(10, 4),
    "close" NUMERIC(10, 4),
    "volume" BIGINT,

    -- Composite primary key on stock_id and timestamp
    CONSTRAINT pk_fact_prices PRIMARY KEY (stock_id, "timestamp"),

     -- Foreign key constraint to dim_stocks
    CONSTRAINT fk_dim_stocks FOREIGN KEY (stock_id) REFERENCES dim_stocks(id) 
        ON DELETE CASCADE -- If a stock is deleted from dim_stocks, automatically delete related prices
);

CREATE INDEX idx_fact_prices_timestamp ON fact_prices("timestamp" DESC);