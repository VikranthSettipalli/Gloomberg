import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { Quote, OHLCV } from '@/types';

export function useMarketData() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const getQuote = useCallback(async (symbol: string): Promise<Quote | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Quote>(`/market/quote/${symbol}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getHistory = useCallback(
    async (
      symbol: string,
      start: string,
      end: string,
      interval: string = '1d'
    ): Promise<OHLCV[]> => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get<OHLCV[]>(`/market/history/${symbol}`, {
          params: { start, end, interval },
        });
        return response.data;
      } catch (err) {
        setError(err as Error);
        return [];
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { getQuote, getHistory, loading, error };
}
