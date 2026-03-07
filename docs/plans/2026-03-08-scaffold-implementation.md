# Gloomberg Scaffold Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create complete project structure with interfaces, stubs, and tests for the Gloomberg Bloomberg Terminal alternative.

**Architecture:** Python FastAPI backend with provider pattern for data sources, React/TypeScript frontend with Vite, PostgreSQL + TimescaleDB for persistence. Six service modules (market_data, fundamentals, index, estimates, shareholding, screener) each with abstract base providers and concrete stubs.

**Tech Stack:** Python 3.11+, FastAPI, Pydantic, pytest, React 18, TypeScript, Vite, TradingView Lightweight Charts, pnpm

---

## Task 1: Project Root Files

**Files:**
- Create: `pyproject.toml`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `MEMORY.md`

**Step 1: Create pyproject.toml with Python dependencies and pytest config**

**Step 2: Create .env.example with environment variable names (no values)**

**Step 3: Create .gitignore for Python, Node, IDE files**

**Step 4: Create MEMORY.md with project state**

**Step 5: Initialize git and commit**

---

## Task 2: Shared Pydantic Models

**Files:**
- Create: `services/__init__.py`
- Create: `services/models/__init__.py`
- Create: `services/models/market.py`
- Create: `services/models/fundamentals.py`
- Create: `services/models/index.py`
- Create: `services/models/estimates.py`
- Create: `services/models/shareholding.py`
- Test: `tests/conftest.py`
- Test: `tests/services/models/test_models.py`

---

## Task 3: Market Data Service

**Files:**
- Create: `services/market_data/providers/base.py` (ABC)
- Create: `services/market_data/providers/kite.py`
- Create: `services/market_data/providers/yahoo.py`
- Create: `services/market_data/router.py`
- Create: `services/market_data/cache.py`
- Test: `tests/services/market_data/providers/test_*.py`
- Test: `tests/services/market_data/test_router.py`

---

## Task 4: Fundamentals Service

**Files:**
- Create: `services/fundamentals/providers/base.py` (ABC)
- Create: `services/fundamentals/providers/bse_filings.py`
- Create: `services/fundamentals/providers/sec_edgar.py`
- Create: `services/fundamentals/router.py`
- Create: `services/fundamentals/normalizer.py`
- Test: `tests/services/fundamentals/**`

---

## Task 5: Index Service

**Files:**
- Create: `services/index/providers/base.py` (ABC)
- Create: `services/index/providers/nse_index.py`
- Create: `services/index/providers/yahoo_index.py`
- Create: `services/index/router.py`
- Test: `tests/services/index/**`

---

## Task 6: Estimates Service

**Files:**
- Create: `services/estimates/providers/base.py` (ABC)
- Create: `services/estimates/providers/fmp.py`
- Create: `services/estimates/providers/finnhub.py`
- Create: `services/estimates/router.py`
- Create: `services/estimates/consensus_builder.py`
- Test: `tests/services/estimates/**`

---

## Task 7: Shareholding Service

**Files:**
- Create: `services/shareholding/providers/base.py` (ABC)
- Create: `services/shareholding/providers/bse_shareholding.py`
- Create: `services/shareholding/router.py`
- Test: `tests/services/shareholding/**`

---

## Task 8: Screener Service

**Files:**
- Create: `services/screener/engine.py`
- Create: `services/screener/router.py`
- Test: `tests/services/screener/**`

---

## Task 9: API Gateway

**Files:**
- Create: `gateway/main.py`
- Create: `gateway/config.py`
- Create: `gateway/middleware.py`
- Test: `tests/gateway/test_main.py`

---

## Task 10: Data Pipeline Stubs

**Files:**
- Create: `data_pipeline/daily_refresh.py`
- Create: `data_pipeline/quarterly_filings.py`
- Create: `data_pipeline/index_rebalance.py`

---

## Task 11: Database Schema

**Files:**
- Create: `db/schema.sql`
- Create: `db/migrations/.gitkeep`

---

## Task 12: Frontend Scaffold

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/tsconfig.json`
- Create: `frontend/vite.config.ts`
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/services/api.ts`
- Create: `frontend/src/hooks/*.ts` (6 hooks)
- Create: `frontend/src/components/**` (stubs)
- Create: `frontend/src/App.tsx`
- Create: `frontend/src/main.tsx`

---

## Task 13: Final Integration Test

Run all tests, start backend, verify health endpoint, start frontend.

---

## Summary

| Task | Description |
|------|-------------|
| 1 | Project root files |
| 2 | Shared Pydantic models |
| 3 | Market data service |
| 4 | Fundamentals service |
| 5 | Index service |
| 6 | Estimates service |
| 7 | Shareholding service |
| 8 | Screener service |
| 9 | API Gateway |
| 10 | Data pipeline stubs |
| 11 | Database schema |
| 12 | Frontend scaffold |
| 13 | Integration test |

Total: ~50 files, ~13 commits
