import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { ScreenerQuery, ScreenerResult } from '@/types';

export function useScreener() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const screen = useCallback(async (query: ScreenerQuery): Promise<ScreenerResult[]> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.post<ScreenerResult[]>('/screener/screen', query);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const getAvailableFields = useCallback(async (): Promise<string[]> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<string[]>('/screener/fields');
      return response.data;
    } catch (err) {
      setError(err as Error);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return { screen, getAvailableFields, loading, error };
}
