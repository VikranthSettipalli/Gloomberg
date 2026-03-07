-- Gloomberg Database Schema
-- PostgreSQL + TimescaleDB

-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- ============================================
-- Market Data Tables
-- ============================================

CREATE TABLE IF NOT EXISTS quotes (
    id BIGSERIAL,
    symbol VARCHAR(20) NOT NULL,
    ltp DECIMAL(20, 4) NOT NULL,
    open DECIMAL(20, 4),
    high DECIMAL(20, 4),
    low DECIMAL(20, 4),
    close DECIMAL(20, 4),
    volume BIGINT,
    bid DECIMAL(20, 4),
    ask DECIMAL(20, 4),
    timestamp TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (symbol, timestamp)
);

-- Convert to hypertable for time-series optimization
SELECT create_hypertable('quotes', 'timestamp', if_not_exists => TRUE);

CREATE TABLE IF NOT EXISTS ohlcv_daily (
    symbol VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(20, 4) NOT NULL,
    high DECIMAL(20, 4) NOT NULL,
    low DECIMAL(20, 4) NOT NULL,
    close DECIMAL(20, 4) NOT NULL,
    volume BIGINT NOT NULL,
    PRIMARY KEY (symbol, date)
);

-- ============================================
-- Fundamentals Tables
-- ============================================

CREATE TABLE IF NOT EXISTS financials (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    period VARCHAR(10) NOT NULL,
    fiscal_year INTEGER NOT NULL,
    revenue DECIMAL(20, 2),
    net_income DECIMAL(20, 2),
    ebitda DECIMAL(20, 2),
    eps DECIMAL(10, 4),
    total_assets DECIMAL(20, 2),
    total_liabilities DECIMAL(20, 2),
    total_equity DECIMAL(20, 2),
    operating_cash_flow DECIMAL(20, 2),
    filing_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (symbol, period, fiscal_year)
);

CREATE INDEX idx_financials_symbol ON financials(symbol);

-- ============================================
-- Shareholding Tables
-- ============================================

CREATE TABLE IF NOT EXISTS shareholding (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    year INTEGER NOT NULL,
    filing_date DATE,
    promoter DECIMAL(6, 2),
    fii DECIMAL(6, 2),
    dii DECIMAL(6, 2),
    public DECIMAL(6, 2),
    others DECIMAL(6, 2),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (symbol, quarter, year)
);

CREATE INDEX idx_shareholding_symbol ON shareholding(symbol);

-- ============================================
-- Estimates Tables
-- ============================================

CREATE TABLE IF NOT EXISTS estimates (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    metric VARCHAR(20) NOT NULL,
    period VARCHAR(20) NOT NULL,
    source VARCHAR(50) NOT NULL,
    value DECIMAL(20, 4) NOT NULL,
    basis VARCHAR(20) DEFAULT 'consolidated',
    estimate_date DATE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_estimates_symbol ON estimates(symbol);
CREATE INDEX idx_estimates_period ON estimates(symbol, metric, period);

-- ============================================
-- Index Tables
-- ============================================

CREATE TABLE IF NOT EXISTS index_constituents (
    id BIGSERIAL PRIMARY KEY,
    index_symbol VARCHAR(20) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    weight DECIMAL(6, 4),
    sector VARCHAR(50),
    as_of_date DATE NOT NULL,
    UNIQUE (index_symbol, symbol, as_of_date)
);

CREATE INDEX idx_constituents_index ON index_constituents(index_symbol, as_of_date);

-- ============================================
-- Symbols/Master Table
-- ============================================

CREATE TABLE IF NOT EXISTS symbols (
    symbol VARCHAR(20) PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    exchange VARCHAR(10) NOT NULL,
    sector VARCHAR(50),
    industry VARCHAR(100),
    market_cap_category VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_symbols_exchange ON symbols(exchange);
CREATE INDEX idx_symbols_sector ON symbols(sector);
