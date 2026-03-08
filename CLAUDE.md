# GLOOMBERG — Project Brief

> Bloomberg Terminal alternative — internal tool for equity research and market monitoring.

---

## 1. Project Overview

**Goal:** Build a modular, extensible Bloomberg-like terminal for personal/internal use.

**Universe (Current Scope):**
- Indian equities (NSE / BSE) — primary focus
- US equities — secondary
- Global / multi-market — future extension

**Out of Scope (for now):**
- Fixed income / bonds
- Commodities
- Forex

**Project Location:** `E:\Claude Projects\Coding\Gloomberg`

---

## 2. Core Modules (Bloomberg Screen Mapping)

| # | Module | Bloomberg Equivalent | Description |
|---|--------|---------------------|-------------|
| 1 | **Stock Dashboard** | DES + FA + GP + ANR | Stock description, detailed financials with projections, price & charts, consensus projections, multiples (historical + forward) |
| 2 | **Equity Screener** | EQS | Filter/sort across the entire equity universe by any metric |
| 3 | **Analyst Reports** | ANR / CN | Aggregated analyst reports for a stock |
| 4 | **Shareholding Tracker** | HDS / OWN | Shareholding pattern changes over time (FII, DII, promoter, public) |
| 5 | **Historical Metric Charts** | GF / FA chart toggle | Chart any financial metric historically (revenue, margins, PE, etc.) |


**Build Sequence:**
1. Stock Dashboard (highest daily use, anchors UX)
2. Historical metric charts (reusable charting component)
3. Equity Screener (needs data pipeline first)
4. Shareholding tracker

---

## 3. Data Sources & Provider Strategy

### Design Principle: Adapter Pattern
Every data need has a `providers/` folder. Each provider is a standalone file implementing a common interface. Swapping or adding a source = writing one new file. The router/service layer never knows which provider is active.

### 3.1 Real-Time Market Data

**Primary: Zerodha Kite Connect** (user has active Zerodha account)
- Cost: ₹500/month
- WebSocket streaming (binary, low-latency)
- Up to 3,000 instrument subscriptions per connection
- Data: LTP, OHLC, bid/ask depth (5 levels), volume, OI
- Historical candle data (1min to daily)
- Auth: OAuth redirect flow, daily token refresh needed
- Python SDK: `pykiteconnect`
- JS SDK: `kiteconnectjs`
- Docs: https://kite.trade/docs/connect/v3/
- **Kite MCP server** (`mcp-remote`): Available for interactive market data queries during Claude development sessions. Separate from the programmatic Kite Connect API used by the app backend.

**Fallback/Free: Yahoo Finance (`yfinance`)**
- Cost: Free
- Delay: ~15 minutes
- Good for: historical OHLCV, basic quote data, US/global stocks
- No websocket — polling only

**Provider files needed:**
- `providers/kite.py` — Zerodha real-time + historical
- `providers/yahoo.py` — free fallback, US/global coverage

### 3.2 Fundamentals & Financials

**Indian Stocks:**
- **BSE API** (bseindia.com public JSON API) — quarterly financials, filings, structured data. Free.
- **NSE RSS feeds** — corporate announcements, real-time filings. Free.

**US Stocks:**
- **SEC EDGAR API** — XBRL filings, authoritative, structured. Free with API key.

**Provider files needed:**
- `providers/bse_filings.py` — Indian fundamentals from BSE
- `providers/sec_edgar.py` — US fundamentals from SEC

### 3.3 Index Data

- **NSE official endpoints** — Nifty 50, sectoral indices, constituents
- **Yahoo Finance** — S&P 500, global indices
- `providers/nse_index.py`
- `providers/yahoo_index.py`

### 3.4 Shareholding Patterns

- **BSE API** — quarterly shareholding filings (FII, DII, promoter, public). Structured JSON. Free.
- `providers/bse_shareholding.py`

### 3.5 Macro / Reference Data

- **FRED API** (St. Louis Fed) — US macro data, treasury yields. Free with API key.
- **RBI DBIE** — Indian macro data. Free CSV.
- `providers/fred.py`
- `providers/rbi.py`

### 3.6 Consensus Estimates & Analyst Data (CRITICAL FEATURE)

This is a high-priority feature. The strategy is a two-provider approach for maximum coverage.

**Primary: Financial Modeling Prep (FMP)**
- Free tier: 250 API calls/day (sufficient for single-user local tool)
- Paid Starter: $22/mo for 300 calls/min + 5 years history (upgrade if free tier is limiting)
- Provides: Revenue estimates, EPS forecasts, consensus metrics (avg/high/low/# analysts), price targets, analyst grades (buy/hold/sell), upgrade/downgrade history, earnings calendar, earnings surprises
- Coverage: Strong for US equities. Limited for pure Indian stocks.
- API: REST JSON, no official SDK but straightforward HTTP calls
- Docs: https://site.financialmodelingprep.com/developer/docs
- Key endpoints:
  - `/api/v3/analyst-estimates/{symbol}` — annual/quarterly revenue & EPS estimates
  - `/api/v3/grade/{symbol}` — analyst grades history
  - `/api/v4/price-target-consensus` — price target consensus
  - `/api/v3/earnings-surprises/{symbol}` — historical earnings vs estimates

**Secondary: Finnhub**
- Free tier: 60 API calls/minute
- Provides: Recommendation trends (buy/hold/sell counts — FREE), earnings surprises (FREE), earnings calendar (FREE)
- EPS estimates, revenue estimates, EBITDA estimates, price targets are PREMIUM (paid plan required)
- Coverage: Global, including some Indian ADRs
- Python SDK: `finnhub-python`
- Docs: https://finnhub.io/docs/api
- Key free endpoints:
  - `recommendation_trends(symbol)` — analyst buy/hold/sell consensus
  - `company_earnings(symbol)` — historical earnings surprises
  - `earnings_calendar()` — upcoming earnings dates

**Indian Stock Estimates — Custom Consensus Builder:**
Neither FMP nor Finnhub has deep analyst estimate coverage for pure NSE/BSE-listed Indian companies. Instead of showing "N/A", we build our OWN consensus from available individual analyst estimates.

**Two-track approach:**
1. **Dual-listed / ADR companies** (Infosys, HDFC Bank, ICICI, Wipro, Dr. Reddy's, etc.): Use FMP/Finnhub consensus directly — these are covered by US-side analysts.
2. **Pure domestic Indian stocks**: Build consensus via `consensus_builder.py` — an engine that ingests raw analyst estimates from any source and produces normalized consensus.

**Like-to-like normalization rules (CRITICAL):**
The consensus builder MUST apply these adjustments before averaging:
- **Consolidated vs Standalone**: Prefer consolidated. Flag and exclude standalone estimates unless no consolidated available. Never mix the two.
- **Fiscal year alignment**: Indian FY = Apr-Mar. Some analysts report calendar year. Normalize all estimates to the company's reported fiscal year before comparing.
- **Stock splits & bonus adjustments**: All EPS estimates must be on the SAME share base. If a company did a 1:5 split, historical estimates must be adjusted to post-split basis before comparison.
- **Extraordinary / exceptional items**: Strip one-off items (asset sales, write-downs, merger costs) to get to operating/recurring estimates. Flag adjusted vs reported basis clearly.
- **Currency normalization**: Should not be an issue for Indian stocks (all INR), but important if comparing with ADR estimates (USD → INR conversion at estimate-date FX rate).
- **Recency weighting**: Recent estimates matter more. Apply time-decay weighting — e.g., an estimate from 2 weeks ago gets more weight than one from 6 months ago. Suggested: exponential decay with half-life of 60 days.
- **Outlier handling**: Use trimmed mean (drop top and bottom 10%) rather than simple average to avoid skew from stale or extreme estimates. If <5 estimates, use median instead.

**Raw estimate input sources (pluggable):**
- Manual entry via simple UI form (reading broker research PDFs and entering key numbers)
- CSV/Excel bulk upload (batch entry from multiple reports)
- Future: API integrations with Indian data vendors if available
- Future: NLP extraction from earnings call transcripts and broker report PDFs

**Consensus output schema:**
```json
{
  "ticker": "RELIANCE.NS",
  "metric": "EPS",
  "period": "FY2026E",
  "basis": "consolidated",
  "adjusted": true,
  "share_base_date": "2025-01-01",
  "consensus": {
    "mean": 98.5,
    "trimmed_mean": 97.2,
    "median": 96.8,
    "high": 112.0,
    "low": 85.0,
    "std_dev": 8.3,
    "num_estimates": 12,
    "recency_weighted_mean": 99.1
  },
  "individual_estimates": [
    {"source": "Motilal Oswal", "value": 101.0, "date": "2025-02-15", "basis": "consolidated"},
    {"source": "ICICI Direct", "value": 95.0, "date": "2025-01-20", "basis": "consolidated"}
  ],
  "last_updated": "2025-03-01"
}
```

**Provider files needed:**
- `providers/fmp.py` — FMP estimates, grades, price targets (US + dual-listed)
- `providers/finnhub.py` — recommendation trends, earnings surprises (supplementary)
- `providers/manual_estimates.py` — manual/CSV input for Indian stocks
- `consensus_builder.py` — normalization engine + weighted averaging logic

**Cost Tiers:**

| Tier | Sources | Cost | What You Get |
|------|---------|------|-------------|
| Free | FMP free + Finnhub free | $0 | 250 FMP calls/day + 60 Finnhub calls/min. Enough for single-user local tool |
| Standard | FMP Starter + Finnhub free | ~$22/mo (~₹1,800) | Higher rate limits, 5yr history, cross-validated data |
| Full | FMP Starter + Finnhub paid | Variable | Complete estimates + price targets + EBITDA estimates |

### 3.7 Remaining Data Gaps

| Data Need | Status | Workaround |
|-----------|--------|------------|
| Analyst reports (full text) | **Always paywalled** | Link aggregation only, no full text |
| True real-time tick data (without broker account) | **Paid only** | Zerodha Kite covers this |

---

## 4. Architecture

### 4.1 High-Level Structure

```
gloomberg/
├── CLAUDE.md                        # This file — project context
│
├── services/                        # Backend service modules
│   ├── market_data/                 # Prices, OHLCV, live quotes
│   │   ├── providers/
│   │   │   ├── base.py              # Abstract provider interface
│   │   │   ├── kite.py              # Zerodha Kite Connect (real-time)
│   │   │   └── yahoo.py             # Yahoo Finance (free fallback)
│   │   ├── router.py                # Unified API: /quote, /history, /intraday
│   │   ├── cache.py                 # In-memory / Redis cache layer
│   │   └── websocket_manager.py     # WebSocket connection lifecycle
│   │
│   ├── fundamentals/                # Financials, ratios, filings
│   │   ├── providers/
│   │   │   ├── base.py
│   │   │   ├── bse_filings.py       # BSE structured filings (India)
│   │   │   └── sec_edgar.py         # SEC XBRL (US)
│   │   ├── router.py                # /financials, /ratios, /filings
│   │   └── normalizer.py            # Map different schemas → common format
│   │
│   ├── index/                       # Index data, constituents, sectors
│   │   ├── providers/
│   │   │   ├── nse_index.py
│   │   │   └── yahoo_index.py
│   │   └── router.py                # /indices, /constituents, /sector-perf
│   │
│   ├── estimates/                   # Consensus estimates & analyst data
│   │   ├── providers/
│   │   │   ├── base.py
│   │   │   ├── fmp.py               # Financial Modeling Prep (US + dual-listed)
│   │   │   ├── finnhub.py           # Finnhub (supplementary — free tier)
│   │   │   └── manual_estimates.py  # Manual/CSV input for Indian stocks
│   │   ├── router.py                # /estimates, /price-targets, /recommendations
│   │   ├── consensus_builder.py     # Like-to-like normalization + weighted averaging
│   │   └── normalizer.py            # Merge all sources into unified schema
│   │
│   ├── shareholding/                # Ownership & changes over time
│   │   ├── providers/
│   │   │   └── bse_shareholding.py
│   │   └── router.py                # /shareholding/{ticker}/history
│   │
│   └── screener/                    # Equity screening engine
│       ├── engine.py                # Filter/sort/rank logic
│       ├── router.py                # /screen with filter params
│       └── precompute.py            # Scheduled job to cache universe metrics
│
├── gateway/                         # API Gateway
│   ├── main.py                      # FastAPI app, mounts all service routers
│   ├── middleware.py                # Rate limiting, CORS, auth
│   └── config.py                    # Environment config, API keys, provider selection
│
├── frontend/                        # React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── StockDashboard/      # Module 1: main stock view
│   │   │   ├── ChartPanel/          # Reusable charting (TradingView Lightweight Charts)
│   │   │   ├── EstimatesPanel/      # Consensus estimates, price targets, analyst grades
│   │   │   ├── ScreenerTable/       # Module 2: equity screener
│   │   │   ├── ShareholdingView/    # Module 4: ownership tracker
│   │   │   ├── MetricCharts/        # Module 5: historical metric charting
│   │   │   └── common/              # Shared UI: tables, inputs, layout
│   │   ├── hooks/
│   │   │   ├── useMarketData.ts     # Calls market_data service
│   │   │   ├── useFundamentals.ts   # Calls fundamentals service
│   │   │   ├── useEstimates.ts      # Calls estimates service
│   │   │   ├── useIndex.ts          # Calls index service
│   │   │   ├── useShareholding.ts   # Calls shareholding service
│   │   │   └── useScreener.ts       # Calls screener service
│   │   ├── services/                # API client layer (axios/fetch wrappers)
│   │   └── App.tsx
│   └── package.json
│
├── data_pipeline/                   # Scheduled / batch jobs
│   ├── daily_refresh.py             # EOD data pull & cache warm
│   ├── quarterly_filings.py         # Shareholding + financials refresh
│   └── index_rebalance.py           # Index constituent updates
│
├── db/                              # Database
│   ├── schema.sql
│   └── migrations/
│
├── .env.example                     # API keys template
└── requirements.txt
```

### 4.2 Key Design Principles

1. **Adapter pattern for all data providers.** Every provider implements the same interface (`base.py`). Adding a new data source = one new file, zero changes to router or frontend.

2. **Normalizer layer in fundamentals.** BSE filings and SEC EDGAR have completely different schemas. The normalizer maps everything to a common format so the frontend never knows which source it came from.

3. **Single gateway.** Frontend talks to ONE API endpoint. All service routers are mounted under the FastAPI gateway. Services can be split into actual microservices later if scale demands it.

4. **Provider selection via config.** `.env` or `config.py` controls which provider is active (e.g., `MARKET_DATA_PROVIDER=kite` vs `MARKET_DATA_PROVIDER=yahoo`). No code changes needed to switch.

5. **Cache layer per service.** Market data cache is aggressive (sub-second for live quotes). Fundamentals cache is longer-lived (daily or quarterly refresh).

6. **Frontend hooks map 1:1 to backend services.** Each hook encapsulates all API calls for one domain. Components never call APIs directly.

### 4.3 Tech Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend | Python + FastAPI | Async, fast, great for financial data |
| Real-time | WebSocket (Kite) → FastAPI WebSocket → Frontend | End-to-end streaming |
| Frontend | React + TypeScript | Component reusability, type safety |
| Charts | TradingView Lightweight Charts | Free, Bloomberg-like, performant |
| Database | PostgreSQL + TimescaleDB extension | Time-series optimized for historical metrics |
| Cache | Redis (or in-memory for MVP) | Low-latency quote caching |
| Scheduling | APScheduler or Celery (later) | Data pipeline jobs |

---

## 5. Authentication & API Keys Required

| Service | Key Needed | How to Get |
|---------|-----------|------------|
| Zerodha Kite Connect | `api_key` + `api_secret` | https://developers.kite.trade — ₹500/mo subscription |
| Financial Modeling Prep | `api_key` | https://site.financialmodelingprep.com/register — free tier (250 calls/day) |
| Finnhub | `api_key` | https://finnhub.io/register — free tier (60 calls/min) |
| SEC EDGAR | User-Agent header (email) | Free, just register email |
| FRED | API key | https://fred.stlouisfed.org/docs/api/api_key.html — free |
| Yahoo Finance | None | `yfinance` uses unofficial API, no key needed |
| BSE | None | Public JSON endpoints |
| NSE | None | Public endpoints (rate-limit cautiously) |

---

## 6. Resolved Decisions

- [x] **Deployment**: Local-only tool. No VPS, no cloud deployment.
- [x] **Multi-user**: Single user (personal tool). No auth system needed.
- [x] **Consensus estimates**: Two-provider strategy — FMP (primary) + Finnhub (supplementary). Start with free tiers, upgrade FMP to Starter ($22/mo) if needed.
- [x] **No scraping**: All data from official APIs, exchange filings, and licensed broker feeds only.
- [x] **Fixed income**: Removed from scope.
- [x] **Frontend**: React SPA (not Next.js). TypeScript + TradingView Lightweight Charts.
- [x] **Analyst reports**: Skip for MVP. Defer to future versions.
- [x] **Indian estimates**: No manual entry. Future: automated broker PDF ingestion + LLM extraction + normalization + consensus + projections. Deferred to v2+.

---

## 8. Development Guidelines

- **Do NOT scrape** websites like Screener.in, Trendlyne, Moneycontrol, etc. Use only official APIs, exchange data, and licensed feeds.
- **Provider-first thinking**: Before adding any data feature, first create the provider, then the router, then the frontend hook, then the component.
- **Type everything**: Use Pydantic models on the backend, TypeScript interfaces on the frontend. Shared schema definitions where possible.
- **Test providers independently**: Each provider should be testable standalone with a simple script.
- **Rate limit awareness**: NSE endpoints are aggressive with rate limits. BSE is more lenient. Yahoo Finance has unofficial limits (~2000 requests/hour). Kite has documented limits per the subscription.

---

## 9. How Competitors Get Real-Time Data (Context)

For reference — this is how the platforms we're trying to replicate source their data:

- **Bloomberg**: Direct co-located exchange connections globally. Licensed L1/L2 tick data. Pays millions/year. Own analyst estimate aggregation (BEST).
- **Trendlyne / Screener.in**: Licensed NSE/BSE data feeds through authorized vendors (TrueData, GlobalDataFeeds, etc.). Vendor licenses cost ~₹5-15 lakhs/year. Fundamental data parsed from BSE/MCA XBRL filings.
- **Our approach**: Zerodha Kite Connect (₹500/mo, real-time via broker API) + BSE/SEC public filings for fundamentals. Legal for personal/internal use. Not redistributable without exchange vendor license.

---

## 10. Monthly Running Cost Summary

| Service | Free Tier | Paid Tier (if needed) |
|---------|-----------|----------------------|
| Zerodha Kite Connect | — | ₹500/mo (required for real-time) |
| Financial Modeling Prep | 250 calls/day | $22/mo (~₹1,800) for Starter |
| Finnhub | 60 calls/min | Paid plans available |
| Yahoo Finance | Free | — |
| BSE / NSE / SEC EDGAR / FRED | Free | — |
| **Total (minimum)** | **₹500/mo** | — |
| **Total (recommended)** | **~₹2,300/mo** | Kite + FMP Starter |

---

## 11. Deferred Features (Future Versions)

| Feature | Description | Complexity |
|---------|-------------|------------|
| Analyst Reports (Module 5) | Link aggregation — report metadata (title, date, broker, rating) with links. No full text. | Medium |
| Automated Indian Consensus Builder | Ingest broker research PDFs → LLM-powered extraction of key estimates → like-to-like normalization → weighted consensus → forward projections. Replaces manual entry entirely. | High |

---

## 12. Milestone 1 Implementation Log (Stock Terminal Page)

**Date:** 2026-03-08
**Status:** Functional MVP — all core features working

### Scope Decisions (Confirmed with User)

- **Market Data Provider**: Yahoo Finance (`yfinance`) as primary — free, global coverage, no API key needed
- **Fundamentals Provider**: Yahoo Finance (FMP deferred — start without API key)
- **Database**: SQLite for MVP (PostgreSQL/TimescaleDB deferred)
- **Deployment**: Local only, no Docker — `uvicorn` backend + `vite` frontend dev server
- **Priority**: Stock Terminal Page first, then Analyst Data, Screener, Financial Modeling
- **Universe**: Global equities — AAPL, MSFT, TSLA, RELIANCE.NS, GOOGL all supported
- **UI**: Dark theme, information-dense, inspired by Bloomberg/Screener.in

### What Was Built

**Backend (Python/FastAPI):**

- Full Yahoo Finance provider (`services/market_data/providers/yahoo.py`) with:
  - Ticker search via Yahoo Finance search API
  - Real-time quotes from `yfinance` (ticker.info + fast_info fallback)
  - Historical OHLCV data (1m to monthly intervals)
  - Company profile (sector, industry, country, employees, description)
  - Income statements (annual + quarterly) from ticker.financials
  - Balance sheets from ticker.balance_sheet
  - Cash flow statements from ticker.cashflow
  - Financial ratios and valuation multiples from ticker.info
- Updated market data router with new endpoints:
  - `GET /market/search?q=` — instrument search
  - `GET /market/quote/{symbol}` — real-time quote
  - `GET /market/history/{symbol}?start=&end=&interval=` — OHLCV history
  - `GET /market/profile/{symbol}` — company profile
  - `GET /market/ratios/{symbol}` — valuation ratios
  - `GET /market/income-statement/{symbol}?period=` — income statements
  - `GET /market/balance-sheet/{symbol}?period=` — balance sheets
  - `GET /market/cash-flow/{symbol}?period=` — cash flow statements
- Routes use `{symbol:path}` for dot-containing symbols (e.g., RELIANCE.NS)
- `asyncio.to_thread()` wraps blocking yfinance calls for async FastAPI

**Frontend (React/TypeScript/Vite):**

- **StockDashboard**: Main stock page — search bar, fetches quote + profile + ratios in parallel
- **QuoteCard**: Stock price, change, open/high/low/close, 52-week range, market cap, P/E, volume
- **ChartPanel**: TradingView Lightweight Charts candlestick chart with period toggles (1D/1W/1M/3M/1Y)
- **ValuationPanel**: Trailing multiples, forward multiples, profitability metrics (margins, ROE, ROA, D/E)
- **FinancialsPanel**: Tabbed income statement / balance sheet / cash flow with annual/quarterly toggle
- **TickerSearch**: Autocomplete search with debounce
- **useMarketData hook**: All API calls for market data service
- Landing page with GLOOMBERG hero and quick-access ticker buttons

### Key Technical Fixes

1. **Decimal → float serialization**: Pydantic v2 serializes `Decimal` as strings in JSON. Changed all models from `Decimal` to `float` to ensure frontend receives proper numbers.
2. **Frontend Number() safety**: All formatting functions (`fmtNum`, `fmtPct`, `fmtLarge`, `fmt`) accept `number | string` and convert with `Number()` for robustness.
3. **Chart data validation**: Filter out invalid OHLCV entries (zero/negative prices) before passing to TradingView.
4. **CORS**: Updated to allow ports 5173, 5174, 5175.
5. **Rollup native dependency**: Required clean `rm -rf node_modules && npm install` to resolve `@rollup/rollup-win32-x64-msvc` missing module.

### Running the Application

```bash
# Backend (from project root)
python -m uvicorn gateway.main:app --host 0.0.0.0 --port 8000

# Frontend (from frontend/)
npm install
npx vite --port 5174 --host

# Access at http://localhost:5174
```

### What's Next (Milestone 2+)

- Analyst Data Screen (estimates, price targets, recommendations)
- Equity Screener
- UI polish: company description panel, improved dark theme
- SQLite persistence for cached data
- Historical metric charting
