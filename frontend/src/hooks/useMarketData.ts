import { useState, useCallback } from 'react';
import api from '@/services/api';
import type {
  Quote, OHLCV, Instrument, CompanyProfile, Ratios,
  IncomeStatement, BalanceSheet, CashFlowStatement,
} from '@/types';

export function useMarketData() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const searchInstruments = useCallback(
    async (query: string): Promise<Instrument[]> => {
      if (query.length < 1) return [];
      try {
        const response = await api.get<Instrument[]>('/market/search', {
          params: { q: query },
        });
        return response.data;
      } catch (err) {
        console.error('Search failed:', err);
        return [];
      }
    },
    []
  );

  const getQuote = useCallback(async (symbol: string): Promise<Quote | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Quote>(`/market/quote/${encodeURIComponent(symbol)}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getHistory = useCallback(
    async (symbol: string, start: string, end: string, interval: string = '1d'): Promise<OHLCV[]> => {
      try {
        const response = await api.get<OHLCV[]>(`/market/history/${encodeURIComponent(symbol)}`, {
          params: { start, end, interval },
        });
        return response.data;
      } catch (err) {
        console.error('History failed:', err);
        return [];
      }
    },
    []
  );

  const getProfile = useCallback(async (symbol: string): Promise<CompanyProfile | null> => {
    try {
      const response = await api.get<CompanyProfile>(`/market/profile/${encodeURIComponent(symbol)}`);
      return response.data;
    } catch (err) {
      console.error('Profile failed:', err);
      return null;
    }
  }, []);

  const getRatios = useCallback(async (symbol: string): Promise<Ratios | null> => {
    try {
      const response = await api.get<Ratios>(`/market/ratios/${encodeURIComponent(symbol)}`);
      return response.data;
    } catch (err) {
      console.error('Ratios failed:', err);
      return null;
    }
  }, []);

  const getIncomeStatements = useCallback(
    async (symbol: string, period: string = 'annual'): Promise<IncomeStatement[]> => {
      try {
        const response = await api.get<IncomeStatement[]>(
          `/market/income-statement/${encodeURIComponent(symbol)}`,
          { params: { period } }
        );
        return response.data;
      } catch (err) {
        console.error('Income statement failed:', err);
        return [];
      }
    },
    []
  );

  const getBalanceSheets = useCallback(
    async (symbol: string, period: string = 'annual'): Promise<BalanceSheet[]> => {
      try {
        const response = await api.get<BalanceSheet[]>(
          `/market/balance-sheet/${encodeURIComponent(symbol)}`,
          { params: { period } }
        );
        return response.data;
      } catch (err) {
        console.error('Balance sheet failed:', err);
        return [];
      }
    },
    []
  );

  const getCashFlowStatements = useCallback(
    async (symbol: string, period: string = 'annual'): Promise<CashFlowStatement[]> => {
      try {
        const response = await api.get<CashFlowStatement[]>(
          `/market/cash-flow/${encodeURIComponent(symbol)}`,
          { params: { period } }
        );
        return response.data;
      } catch (err) {
        console.error('Cash flow failed:', err);
        return [];
      }
    },
    []
  );

  return {
    searchInstruments, getQuote, getHistory, getProfile, getRatios,
    getIncomeStatements, getBalanceSheets, getCashFlowStatements,
    loading, error,
  };
}
