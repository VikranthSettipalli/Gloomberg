import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { Shareholding } from '@/types';

export function useShareholding() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const getShareholding = useCallback(async (symbol: string): Promise<Shareholding | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Shareholding>(`/shareholding/${symbol}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getShareholdingHistory = useCallback(async (symbol: string): Promise<Shareholding[]> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Shareholding[]>(`/shareholding/${symbol}/history`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return { getShareholding, getShareholdingHistory, loading, error };
}
