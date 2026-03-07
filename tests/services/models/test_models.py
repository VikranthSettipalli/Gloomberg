"""Tests for Pydantic models."""
import pytest
from datetime import datetime, date
from decimal import Decimal

from services.models import (
    Quote,
    OHLCV,
    Financials,
    Ratios,
    IndexData,
    Constituent,
    Estimates,
    Consensus,
    PriceTargets,
    Recommendation,
    Shareholding,
)


class TestMarketModels:
    def test_quote_creation(self, sample_symbol: str, sample_timestamp: datetime):
        quote = Quote(
            symbol=sample_symbol,
            ltp=Decimal("2500.50"),
            timestamp=sample_timestamp,
        )
        assert quote.symbol == sample_symbol
        assert quote.ltp == Decimal("2500.50")

    def test_quote_optional_fields(self, sample_symbol: str, sample_timestamp: datetime):
        quote = Quote(
            symbol=sample_symbol,
            ltp=Decimal("2500.50"),
            open=Decimal("2490.00"),
            high=Decimal("2510.00"),
            low=Decimal("2485.00"),
            volume=1000000,
            timestamp=sample_timestamp,
        )
        assert quote.open == Decimal("2490.00")
        assert quote.volume == 1000000

    def test_ohlcv_creation(self, sample_symbol: str, sample_timestamp: datetime):
        ohlcv = OHLCV(
            symbol=sample_symbol,
            timestamp=sample_timestamp,
            open=Decimal("2490.00"),
            high=Decimal("2510.00"),
            low=Decimal("2485.00"),
            close=Decimal("2500.50"),
            volume=1000000,
        )
        assert ohlcv.close == Decimal("2500.50")
        assert ohlcv.volume == 1000000


class TestFundamentalsModels:
    def test_financials_creation(self, sample_symbol: str):
        financials = Financials(
            symbol=sample_symbol,
            period="Q3",
            fiscal_year=2026,
            revenue=Decimal("250000000000"),
            net_income=Decimal("20000000000"),
        )
        assert financials.period == "Q3"
        assert financials.fiscal_year == 2026

    def test_ratios_creation(self, sample_symbol: str):
        ratios = Ratios(
            symbol=sample_symbol,
            pe_ratio=Decimal("25.5"),
            pb_ratio=Decimal("3.2"),
        )
        assert ratios.pe_ratio == Decimal("25.5")


class TestIndexModels:
    def test_index_data_creation(self, sample_timestamp: datetime):
        index = IndexData(
            symbol="NIFTY50",
            name="Nifty 50",
            value=Decimal("22500.00"),
            change=Decimal("150.25"),
            change_percent=Decimal("0.67"),
            timestamp=sample_timestamp,
        )
        assert index.symbol == "NIFTY50"

    def test_constituent_creation(self):
        constituent = Constituent(
            symbol="RELIANCE.NS",
            name="Reliance Industries",
            weight=Decimal("10.5"),
            sector="Energy",
        )
        assert constituent.weight == Decimal("10.5")


class TestEstimatesModels:
    def test_estimates_creation(self, sample_symbol: str, sample_date: date):
        estimates = Estimates(
            symbol=sample_symbol,
            metric="EPS",
            period="FY2026E",
            consensus=Consensus(
                mean=Decimal("98.5"),
                median=Decimal("97.0"),
                num_estimates=12,
            ),
            last_updated=sample_date,
        )
        assert estimates.consensus.num_estimates == 12

    def test_price_targets_creation(self, sample_symbol: str):
        targets = PriceTargets(
            symbol=sample_symbol,
            mean=Decimal("2800.00"),
            median=Decimal("2750.00"),
            high=Decimal("3200.00"),
            low=Decimal("2400.00"),
            num_analysts=15,
        )
        assert targets.num_analysts == 15

    def test_recommendation_creation(self, sample_symbol: str):
        rec = Recommendation(
            symbol=sample_symbol,
            strong_buy=5,
            buy=10,
            hold=8,
            sell=2,
            strong_sell=0,
        )
        assert rec.buy == 10


class TestShareholdingModels:
    def test_shareholding_creation(self, sample_symbol: str, sample_date: date):
        shareholding = Shareholding(
            symbol=sample_symbol,
            quarter="Q3",
            year=2026,
            filing_date=sample_date,
            promoter=Decimal("50.5"),
            fii=Decimal("25.0"),
            dii=Decimal("15.0"),
            public=Decimal("9.5"),
        )
        assert shareholding.promoter == Decimal("50.5")
        assert shareholding.fii + shareholding.dii == Decimal("40.0")
