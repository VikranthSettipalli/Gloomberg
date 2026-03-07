"""Gateway configuration."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment."""

    # Provider selection
    market_data_provider: str = "yahoo"
    fundamentals_provider: str = "bse_filings"
    index_provider: str = "nse_index"
    estimates_provider: str = "fmp"
    shareholding_provider: str = "bse_shareholding"

    # API Keys (loaded from environment)
    kite_api_key: str | None = None
    kite_api_secret: str | None = None
    fmp_api_key: str | None = None
    finnhub_api_key: str | None = None
    fred_api_key: str | None = None
    sec_edgar_email: str | None = None

    # Database
    database_url: str = "postgresql://localhost:5432/gloomberg"
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"


settings = Settings()
