"""Index data models."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class IndexData(BaseModel):
    """Index quote and summary."""
    symbol: str
    name: str
    value: Decimal
    change: Decimal
    change_percent: Decimal
    timestamp: datetime


class Constituent(BaseModel):
    """Index constituent."""
    symbol: str
    name: str
    weight: Decimal | None = None
    sector: str | None = None
