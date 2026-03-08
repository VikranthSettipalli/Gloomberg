"""Yahoo Finance provider for free global market data."""
import asyncio
import math
from datetime import date, datetime
from typing import AsyncIterator

import yfinance as yf

from .base import MarketDataProvider
from services.models import (
    Quote, OHLCV, Instrument,
    IncomeStatement, BalanceSheet, CashFlowStatement,
    Ratios, CompanyProfile,
)


def _safe_float(val) -> float | None:
    """Safely convert a value to float."""
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return None
        return f
    except (ValueError, TypeError):
        return None


def _safe_int(val) -> int | None:
    """Safely convert to int."""
    if val is None:
        return None
    try:
        f = float(val)
        if math.isnan(f) or math.isinf(f):
            return None
        return int(f)
    except (ValueError, TypeError):
        return None


class YahooProvider(MarketDataProvider):
    """Yahoo Finance market data provider (free, global coverage).

    Covers US, Indian (.NS/.BO), European, and other global equities.
    ~15 minute delay on quotes. No API key needed.
    """

    async def search(self, query: str) -> list[Instrument]:
        """Search for instruments using Yahoo Finance."""
        def _search():
            try:
                import requests
                url = "https://query2.finance.yahoo.com/v1/finance/search"
                params = {
                    "q": query,
                    "quotesCount": 10,
                    "newsCount": 0,
                    "listsCount": 0,
                    "enableFuzzyQuery": True,
                    "quotesQueryId": "tss_match_phrase_query",
                }
                headers = {"User-Agent": "Mozilla/5.0"}
                resp = requests.get(url, params=params, headers=headers, timeout=5)
                data = resp.json()
                results = []
                for item in data.get("quotes", []):
                    if item.get("quoteType") in ("EQUITY", "ETF"):
                        results.append(Instrument(
                            symbol=item.get("symbol", ""),
                            name=item.get("shortname") or item.get("longname", ""),
                            exchange=item.get("exchange", ""),
                            type=item.get("quoteType", "equity").lower(),
                        ))
                return results
            except Exception:
                return []
        return await asyncio.to_thread(_search)

    async def get_quote(self, symbol: str) -> Quote:
        """Get quote from Yahoo Finance."""
        def _fetch():
            ticker = yf.Ticker(symbol)
            info = ticker.info
            if not info or info.get("trailingPegRatio") is None and info.get("regularMarketPrice") is None:
                fi = ticker.fast_info
                ltp = _safe_float(fi.last_price) or 0.0
                prev = _safe_float(fi.previous_close)
                change_val = (ltp - prev) if ltp and prev else None
                change_pct = ((change_val / prev) * 100) if change_val and prev else None
                return Quote(
                    symbol=symbol,
                    name=info.get("shortName") or info.get("longName") or symbol,
                    ltp=ltp,
                    change=_safe_float(change_val),
                    change_percent=_safe_float(change_pct),
                    open=_safe_float(fi.open),
                    high=_safe_float(fi.day_high),
                    low=_safe_float(fi.day_low),
                    close=prev,
                    volume=_safe_int(fi.last_volume),
                    market_cap=_safe_float(fi.market_cap),
                    currency=info.get("currency", "USD"),
                    timestamp=datetime.now(),
                )

            price = _safe_float(info.get("regularMarketPrice") or info.get("currentPrice")) or 0.0
            prev_close = _safe_float(info.get("regularMarketPreviousClose") or info.get("previousClose"))
            change_val = (price - prev_close) if price and prev_close else None
            change_pct = ((change_val / prev_close) * 100) if change_val and prev_close else None

            return Quote(
                symbol=symbol,
                name=info.get("shortName") or info.get("longName") or symbol,
                ltp=price,
                change=_safe_float(change_val),
                change_percent=_safe_float(change_pct),
                open=_safe_float(info.get("regularMarketOpen") or info.get("open")),
                high=_safe_float(info.get("regularMarketDayHigh") or info.get("dayHigh")),
                low=_safe_float(info.get("regularMarketDayLow") or info.get("dayLow")),
                close=prev_close,
                volume=_safe_int(info.get("regularMarketVolume") or info.get("volume")),
                avg_volume=_safe_int(info.get("averageVolume")),
                market_cap=_safe_float(info.get("marketCap")),
                pe_ratio=_safe_float(info.get("trailingPE")),
                week_52_high=_safe_float(info.get("fiftyTwoWeekHigh")),
                week_52_low=_safe_float(info.get("fiftyTwoWeekLow")),
                currency=info.get("currency", "USD"),
                timestamp=datetime.now(),
            )
        return await asyncio.to_thread(_fetch)

    async def get_history(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """Get historical OHLCV data from Yahoo Finance."""
        def _fetch():
            ticker = yf.Ticker(symbol)
            interval_map = {
                "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
                "1h": "1h", "1d": "1d", "1w": "1wk", "1M": "1mo",
            }
            yf_interval = interval_map.get(interval, "1d")
            df = ticker.history(start=str(start), end=str(end), interval=yf_interval)
            if df.empty:
                return []
            results = []
            for idx, row in df.iterrows():
                ts = idx.to_pydatetime() if hasattr(idx, 'to_pydatetime') else datetime.now()
                o = _safe_float(row["Open"]) or 0.0
                h = _safe_float(row["High"]) or 0.0
                lo = _safe_float(row["Low"]) or 0.0
                c = _safe_float(row["Close"]) or 0.0
                vol = _safe_int(row.get("Volume", 0)) or 0
                if o > 0 and h > 0 and lo > 0 and c > 0:
                    results.append(OHLCV(
                        symbol=symbol,
                        timestamp=ts,
                        open=o, high=h, low=lo, close=c,
                        volume=vol,
                    ))
            return results
        return await asyncio.to_thread(_fetch)

    async def get_company_profile(self, symbol: str) -> CompanyProfile:
        """Get company profile information."""
        def _fetch():
            info = yf.Ticker(symbol).info
            return CompanyProfile(
                symbol=symbol,
                name=info.get("shortName") or info.get("longName", symbol),
                sector=info.get("sector"),
                industry=info.get("industry"),
                country=info.get("country"),
                exchange=info.get("exchange"),
                currency=info.get("currency"),
                market_cap=_safe_float(info.get("marketCap")),
                employees=_safe_int(info.get("fullTimeEmployees")),
                description=info.get("longBusinessSummary"),
                website=info.get("website"),
            )
        return await asyncio.to_thread(_fetch)

    async def get_income_statements(
        self, symbol: str, period: str = "annual"
    ) -> list[IncomeStatement]:
        """Get income statements."""
        def _fetch():
            ticker = yf.Ticker(symbol)
            df = ticker.financials if period == "annual" else ticker.quarterly_financials
            if df is None or df.empty:
                return []
            results = []
            for col in df.columns:
                stmt_date = col.date() if hasattr(col, 'date') else col

                def _get(label):
                    return _safe_float(df.loc[label, col]) if label in df.index else None

                rev = _get("Total Revenue")
                cogs = _get("Cost Of Revenue")
                gross = _get("Gross Profit")
                op_inc = _get("Operating Income")
                ni = _get("Net Income")

                gm = (gross / rev * 100) if gross and rev and rev != 0 else None
                om = (op_inc / rev * 100) if op_inc and rev and rev != 0 else None
                nm = (ni / rev * 100) if ni and rev and rev != 0 else None

                results.append(IncomeStatement(
                    symbol=symbol,
                    period=period,
                    date=stmt_date,
                    fiscal_year=stmt_date.year if hasattr(stmt_date, 'year') else None,
                    revenue=rev,
                    cost_of_revenue=cogs,
                    gross_profit=gross,
                    operating_expenses=_get("Operating Expense"),
                    operating_income=op_inc,
                    ebitda=_get("EBITDA"),
                    interest_expense=_get("Interest Expense"),
                    income_before_tax=_get("Pretax Income"),
                    income_tax=_get("Tax Provision"),
                    net_income=ni,
                    eps=_get("Basic EPS"),
                    eps_diluted=_get("Diluted EPS"),
                    gross_margin=gm,
                    operating_margin=om,
                    net_margin=nm,
                ))
            return results
        return await asyncio.to_thread(_fetch)

    async def get_balance_sheets(
        self, symbol: str, period: str = "annual"
    ) -> list[BalanceSheet]:
        """Get balance sheets."""
        def _fetch():
            ticker = yf.Ticker(symbol)
            df = ticker.balance_sheet if period == "annual" else ticker.quarterly_balance_sheet
            if df is None or df.empty:
                return []
            results = []
            for col in df.columns:
                stmt_date = col.date() if hasattr(col, 'date') else col

                def _get(label):
                    return _safe_float(df.loc[label, col]) if label in df.index else None

                results.append(BalanceSheet(
                    symbol=symbol,
                    period=period,
                    date=stmt_date,
                    fiscal_year=stmt_date.year if hasattr(stmt_date, 'year') else None,
                    cash_and_equivalents=_get("Cash And Cash Equivalents"),
                    short_term_investments=_get("Other Short Term Investments"),
                    receivables=_get("Receivables"),
                    inventory=_get("Inventory"),
                    total_current_assets=_get("Current Assets"),
                    property_plant_equipment=_get("Net PPE"),
                    goodwill=_get("Goodwill"),
                    intangible_assets=_get("Other Intangible Assets"),
                    total_assets=_get("Total Assets"),
                    accounts_payable=_get("Accounts Payable"),
                    short_term_debt=_get("Current Debt"),
                    total_current_liabilities=_get("Current Liabilities"),
                    long_term_debt=_get("Long Term Debt"),
                    total_liabilities=_get("Total Liabilities Net Minority Interest"),
                    total_equity=_get("Stockholders Equity"),
                    retained_earnings=_get("Retained Earnings"),
                ))
            return results
        return await asyncio.to_thread(_fetch)

    async def get_cash_flow_statements(
        self, symbol: str, period: str = "annual"
    ) -> list[CashFlowStatement]:
        """Get cash flow statements."""
        def _fetch():
            ticker = yf.Ticker(symbol)
            df = ticker.cashflow if period == "annual" else ticker.quarterly_cashflow
            if df is None or df.empty:
                return []
            results = []
            for col in df.columns:
                stmt_date = col.date() if hasattr(col, 'date') else col

                def _get(label):
                    return _safe_float(df.loc[label, col]) if label in df.index else None

                ocf = _get("Operating Cash Flow")
                capex_val = _get("Capital Expenditure")
                fcf = None
                if ocf is not None and capex_val is not None:
                    fcf = ocf + capex_val

                results.append(CashFlowStatement(
                    symbol=symbol,
                    period=period,
                    date=stmt_date,
                    fiscal_year=stmt_date.year if hasattr(stmt_date, 'year') else None,
                    net_income=_get("Net Income"),
                    depreciation=_get("Depreciation And Amortization"),
                    change_in_working_capital=_get("Change In Working Capital"),
                    operating_cash_flow=ocf,
                    capex=capex_val,
                    investing_cash_flow=_get("Investing Cash Flow"),
                    debt_issued=_get("Issuance Of Debt"),
                    debt_repaid=_get("Repayment Of Debt"),
                    dividends_paid=_get("Common Stock Dividend Paid"),
                    share_buyback=_get("Repurchase Of Capital Stock"),
                    financing_cash_flow=_get("Financing Cash Flow"),
                    free_cash_flow=fcf,
                ))
            return results
        return await asyncio.to_thread(_fetch)

    async def get_ratios(self, symbol: str) -> Ratios:
        """Get financial ratios and valuation multiples."""
        def _fetch():
            info = yf.Ticker(symbol).info
            return Ratios(
                symbol=symbol,
                pe_ratio=_safe_float(info.get("trailingPE")),
                pb_ratio=_safe_float(info.get("priceToBook")),
                ps_ratio=_safe_float(info.get("priceToSalesTrailing12Months")),
                ev_ebitda=_safe_float(info.get("enterpriseToEbitda")),
                ev_sales=_safe_float(info.get("enterpriseToRevenue")),
                forward_pe=_safe_float(info.get("forwardPE")),
                peg_ratio=_safe_float(info.get("pegRatio")),
                roe=_safe_float(info.get("returnOnEquity")),
                roa=_safe_float(info.get("returnOnAssets")),
                gross_margin=_safe_float(info.get("grossMargins")),
                operating_margin=_safe_float(info.get("operatingMargins")),
                net_margin=_safe_float(info.get("profitMargins")),
                debt_to_equity=_safe_float(info.get("debtToEquity")),
                current_ratio=_safe_float(info.get("currentRatio")),
                revenue_per_share=_safe_float(info.get("revenuePerShare")),
                book_value_per_share=_safe_float(info.get("bookValue")),
                enterprise_value=_safe_float(info.get("enterpriseValue")),
                market_cap=_safe_float(info.get("marketCap")),
            )
        return await asyncio.to_thread(_fetch)

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        """Yahoo does not support streaming."""
        raise NotImplementedError("YahooProvider does not support real-time streaming")
        yield  # type: ignore
