# Gloomberg — Project Memory

## Stack
- Backend: Python 3.11+, FastAPI, Pydantic
- Frontend: React 18, TypeScript, Vite, TradingView Lightweight Charts
- Database: PostgreSQL + TimescaleDB
- Testing: pytest + pytest-asyncio + pytest-cov

## Key Paths
- Services: `services/<name>/providers/base.py` (interfaces)
- Gateway: `gateway/main.py` (FastAPI app)
- Frontend: `frontend/src/`
- Tests: `tests/` (mirrors services/)

## Active Task
- Scaffold creation complete

## Decisions
- Provider pattern for all data sources
- Single gateway mounts all service routers
- Frontend hooks map 1:1 to backend services

## Gotchas
- NSE endpoints aggressive with rate limits
- Kite requires daily token refresh
- Yahoo Finance has unofficial ~2000 req/hour limit
