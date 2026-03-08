"""FastAPI gateway - main application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware import TimingMiddleware
from services.market_data import router as market_router
from services.fundamentals import router as fundamentals_router
from services.index import router as index_router
from services.estimates import router as estimates_router
from services.shareholding import router as shareholding_router
from services.screener import router as screener_router

app = FastAPI(
    title="Gloomberg API",
    description="Bloomberg Terminal alternative - internal tool for equity research",
    version="0.1.0",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TimingMiddleware)

# Mount all service routers
app.include_router(market_router)
app.include_router(fundamentals_router)
app.include_router(index_router)
app.include_router(estimates_router)
app.include_router(shareholding_router)
app.include_router(screener_router)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """API root - returns available endpoints."""
    return {
        "name": "Gloomberg API",
        "version": "0.1.0",
        "endpoints": {
            "market_data": "/market",
            "fundamentals": "/fundamentals",
            "indices": "/indices",
            "estimates": "/estimates",
            "shareholding": "/shareholding",
            "screener": "/screener",
        },
    }
