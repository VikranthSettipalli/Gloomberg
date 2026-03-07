import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { Financials, Ratios } from '@/types';

export function useFundamentals() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const getFinancials = useCallback(
    async (symbol: string, period: string = 'quarterly'): Promise<Financials[]> => {
      setLoading(true);
      setError(null);
      try {
        const response = await api.get<Financials[]>(`/fundamentals/financials/${symbol}`, {
          params: { period },
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

  const getRatios = useCallback(async (symbol: string): Promise<Ratios | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Ratios>(`/fundamentals/ratios/${symbol}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { getFinancials, getRatios, loading, error };
}
