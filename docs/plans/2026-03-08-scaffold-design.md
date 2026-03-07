# Gloomberg Scaffold Design

**Date:** 2026-03-08
**Status:** Approved
**Scope:** Full project scaffold with interfaces, stubs, and tests

---

## Overview

Create complete project structure for Gloomberg — a Bloomberg Terminal alternative for equity research. This scaffold establishes all directories, base interfaces, provider stubs, API routes, frontend hooks, and unit tests without implementing working functionality.

## Decisions

| Decision | Choice |
|----------|--------|
| Scope | Full scaffold only (no working implementations) |
| Python testing | pytest + pytest-asyncio + pytest-cov |
| Frontend tooling | Vite |
| Package management | pip + pyproject.toml (Python), pnpm (JS) |

## Architecture

### Backend (Python/FastAPI)

Six service modules under `services/`:

| Service | Providers | Purpose |
|---------|-----------|---------|
| `market_data` | kite, yahoo | Prices, OHLCV, live quotes |
| `fundamentals` | bse_filings, sec_edgar | Financials, ratios, filings |
| `index` | nse_index, yahoo_index | Index data, constituents |
| `estimates` | fmp, finnhub | Consensus estimates, price targets |
| `shareholding` | bse_shareholding | Ownership patterns |
| `screener` | (internal engine) | Filter/sort/rank equities |

Each service structure:
```
services/<name>/
├── providers/
│   ├── base.py          # Abstract interface (ABC)
│   └── <provider>.py    # Provider stub
├── router.py            # FastAPI router
├── cache.py             # Cache layer (where applicable)
└── normalizer.py        # Schema normalization (where applicable)
```

Central gateway:
```
gateway/
├── main.py              # FastAPI app, mounts all routers
├── middleware.py        # CORS, rate limiting
└── config.py            # Environment config, provider selection
```

### Frontend (React/TypeScript/Vite)

```
frontend/
├── src/
│   ├── components/
│   │   ├── StockDashboard/
│   │   ├── ChartPanel/
│   │   ├── EstimatesPanel/
│   │   ├── ScreenerTable/
│   │   ├── ShareholdingView/
│   │   ├── MetricCharts/
│   │   └── common/
│   ├── hooks/
│   │   ├── useMarketData.ts
│   │   ├── useFundamentals.ts
│   │   ├── useEstimates.ts
│   │   ├── useIndex.ts
│   │   ├── useShareholding.ts
│   │   └── useScreener.ts
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### Database

```
db/
├── schema.sql           # PostgreSQL + TimescaleDB schema
└── migrations/          # Migration files (empty for now)
```

### Data Pipeline

```
data_pipeline/
├── daily_refresh.py     # EOD data pull stub
├── quarterly_filings.py # Filings refresh stub
└── index_rebalance.py   # Index updates stub
```

### Testing

```
tests/
├── conftest.py          # Shared fixtures
├── services/
│   ├── market_data/
│   │   ├── test_router.py
│   │   └── providers/
│   │       ├── test_kite.py
│   │       └── test_yahoo.py
│   ├── fundamentals/
│   │   └── ...
│   └── ...
└── gateway/
    └── test_main.py
```

## Provider Interfaces

### MarketDataProvider (ABC)

```python
async def get_quote(self, symbol: str) -> Quote
async def get_history(self, symbol: str, start: date, end: date, interval: str) -> list[OHLCV]
async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]
```

### FundamentalsProvider (ABC)

```python
async def get_financials(self, symbol: str, period: str) -> Financials
async def get_ratios(self, symbol: str) -> Ratios
async def get_filings(self, symbol: str, filing_type: str) -> list[Filing]
```

### IndexProvider (ABC)

```python
async def get_index(self, index_symbol: str) -> IndexData
async def get_constituents(self, index_symbol: str) -> list[Constituent]
```

### EstimatesProvider (ABC)

```python
async def get_estimates(self, symbol: str) -> Estimates
async def get_price_targets(self, symbol: str) -> PriceTargets
async def get_recommendations(self, symbol: str) -> Recommendations
```

### ShareholdingProvider (ABC)

```python
async def get_shareholding(self, symbol: str) -> Shareholding
async def get_shareholding_history(self, symbol: str) -> list[Shareholding]
```

## Pydantic Models

All data types defined in `services/models/`:
- `Quote`, `OHLCV`, `Financials`, `Ratios`, `Filing`
- `IndexData`, `Constituent`, `Estimates`, `PriceTargets`
- `Recommendations`, `Shareholding`

## Out of Scope

- Working API calls (providers raise `NotImplementedError`)
- Database migrations (schema.sql only)
- Real UI components (typed stubs only)
- Docker/deployment (local-only per spec)
- Authentication (single-user per spec)

## Next Steps

1. Execute scaffold creation via implementation plan
2. After scaffold complete, implement Module 1 (Stock Dashboard) with real providers
