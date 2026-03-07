"""Shareholding providers."""
from .base import ShareholdingProvider
from .bse_shareholding import BSEShareholdingProvider

__all__ = ["ShareholdingProvider", "BSEShareholdingProvider"]
