import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { IndexData, Constituent } from '@/types';

export function useIndex() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const getIndex = useCallback(async (indexSymbol: string): Promise<IndexData | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<IndexData>(`/indices/${indexSymbol}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getConstituents = useCallback(async (indexSymbol: string): Promise<Constituent[]> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Constituent[]>(`/indices/${indexSymbol}/constituents`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return { getIndex, getConstituents, loading, error };
}
