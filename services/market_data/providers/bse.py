"""BSE India provider for market data."""
from datetime import date, datetime
from decimal import Decimal
from typing import AsyncIterator
import httpx

from .base import MarketDataProvider
from services.models import Quote, OHLCV, Instrument


class BSEProvider(MarketDataProvider):
    """BSE India market data provider.

    Uses BSE's public API endpoints for:
    - Instrument search
    - Real-time quotes
    - Historical OHLCV data

    No API key required. Rate limit cautiously.
    """

    BASE_URL = "https://api.bseindia.com/BseIndiaAPI/api"

    # Common headers to mimic browser requests
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.bseindia.com/",
        "Origin": "https://www.bseindia.com",
    }

    def __init__(self):
        self._client: httpx.AsyncClient | None = None
        # Cache symbol -> scrip_code mappings
        self._scrip_cache: dict[str, str] = {}

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=30.0,
                follow_redirects=True,
            )
        return self._client

    async def search(self, query: str) -> list[Instrument]:
        """Search for instruments by name or symbol.

        Args:
            query: Search term (e.g., "RELIANCE", "Infosys")

        Returns:
            List of matching instruments
        """
        client = await self._get_client()
        url = f"{self.BASE_URL}/Suggest/w"

        try:
            response = await client.get(url, params={"text": query})
            response.raise_for_status()
            data = response.json()

            instruments = []
            for item in data:
                # BSE returns: "scripcode|symbol|issuer_name|group|type|status"
                parts = item.split("|")
                if len(parts) >= 3:
                    scrip_code = parts[0].strip()
                    symbol = parts[1].strip()
                    name = parts[2].strip()

                    # Cache the mapping
                    self._scrip_cache[symbol.upper()] = scrip_code

                    instruments.append(Instrument(
                        symbol=symbol,
                        name=name,
                        scrip_code=scrip_code,
                        exchange="BSE",
                    ))

            return instruments[:10]  # Limit results

        except httpx.HTTPError as e:
            raise RuntimeError(f"BSE search failed: {e}")

    async def _get_scrip_code(self, symbol: str) -> str:
        """Get BSE scrip code for a symbol."""
        symbol_upper = symbol.upper()

        # Check cache first
        if symbol_upper in self._scrip_cache:
            return self._scrip_cache[symbol_upper]

        # Search for the symbol
        results = await self.search(symbol_upper)
        for inst in results:
            if inst.symbol.upper() == symbol_upper:
                return inst.scrip_code

        if results:
            # Return first match if exact match not found
            return results[0].scrip_code

        raise ValueError(f"Symbol not found: {symbol}")

    async def get_quote(self, symbol: str) -> Quote:
        """Get real-time quote from BSE.

        Args:
            symbol: Stock symbol (e.g., "RELIANCE")
        """
        client = await self._get_client()
        scrip_code = await self._get_scrip_code(symbol)

        url = f"{self.BASE_URL}/getScripHeaderData/w"

        try:
            response = await client.get(
                url,
                params={"Ession": "C", "scripcode": scrip_code}
            )
            response.raise_for_status()
            data = response.json()

            # BSE returns nested structure
            header = data.get("Header", {})

            # Parse values, handling Indian number format (commas)
            def parse_decimal(val) -> Decimal | None:
                if val is None or val == "" or val == "-":
                    return None
                try:
                    # Remove commas from Indian number format
                    clean = str(val).replace(",", "")
                    return Decimal(clean)
                except:
                    return None

            def parse_int(val) -> int | None:
                if val is None or val == "" or val == "-":
                    return None
                try:
                    clean = str(val).replace(",", "")
                    return int(float(clean))
                except:
                    return None

            ltp = parse_decimal(header.get("LTP") or header.get("CurrRate"))
            prev_close = parse_decimal(header.get("PrevClose") or header.get("Prev"))

            change = None
            change_percent = None
            if ltp is not None and prev_close is not None and prev_close != 0:
                change = ltp - prev_close
                change_percent = (change / prev_close) * 100

            return Quote(
                symbol=symbol.upper(),
                name=header.get("ScripName") or header.get("Issuer"),
                ltp=ltp or Decimal("0"),
                change=change,
                change_percent=change_percent,
                open=parse_decimal(header.get("Open")),
                high=parse_decimal(header.get("High")),
                low=parse_decimal(header.get("Low")),
                close=prev_close,
                volume=parse_int(header.get("TotVol") or header.get("Volume")),
                timestamp=datetime.now(),
            )

        except httpx.HTTPError as e:
            raise RuntimeError(f"BSE quote failed: {e}")

    async def get_history(
        self,
        symbol: str,
        start: date,
        end: date,
        interval: str = "1d",
    ) -> list[OHLCV]:
        """Get historical OHLCV data from BSE.

        Note: BSE's public API has limited historical data.
        For better historical data, consider Yahoo Finance.
        """
        client = await self._get_client()
        scrip_code = await self._get_scrip_code(symbol)

        # BSE StockReachGraph endpoint for historical data
        url = f"{self.BASE_URL}/StockReachGraph/w"

        try:
            response = await client.get(
                url,
                params={
                    "scripcode": scrip_code,
                    "flag": "0",
                    "fromdate": start.strftime("%Y%m%d"),
                    "todate": end.strftime("%Y%m%d"),
                    "seression": "Day",
                }
            )
            response.raise_for_status()
            data = response.json()

            candles = []

            # Parse the response - BSE returns Data array
            raw_data = data.get("Data", [])

            for item in raw_data:
                try:
                    # Parse date from various possible formats
                    date_str = item.get("dttm") or item.get("Date")
                    if not date_str:
                        continue

                    # Try parsing different date formats
                    try:
                        ts = datetime.strptime(date_str[:10], "%Y-%m-%d")
                    except:
                        try:
                            ts = datetime.strptime(date_str[:10], "%d-%m-%Y")
                        except:
                            continue

                    def parse_val(key):
                        val = item.get(key, 0)
                        if isinstance(val, str):
                            val = val.replace(",", "")
                        return Decimal(str(val or 0))

                    candles.append(OHLCV(
                        symbol=symbol.upper(),
                        timestamp=ts,
                        open=parse_val("open") or parse_val("Open"),
                        high=parse_val("high") or parse_val("High"),
                        low=parse_val("low") or parse_val("Low"),
                        close=parse_val("close") or parse_val("Close") or parse_val("Price"),
                        volume=int(float(str(item.get("volume") or item.get("Volume") or 0).replace(",", ""))),
                    ))
                except Exception:
                    continue

            # Sort by date ascending
            candles.sort(key=lambda x: x.timestamp)
            return candles

        except httpx.HTTPError as e:
            raise RuntimeError(f"BSE history failed: {e}")

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        """BSE does not support real-time streaming."""
        raise NotImplementedError("BSE does not support real-time streaming. Use Kite for streaming.")
        yield  # type: ignore

    async def close(self):
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
