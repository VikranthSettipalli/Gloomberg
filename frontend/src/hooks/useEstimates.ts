import { useState, useCallback } from 'react';
import api from '@/services/api';
import type { Estimates, PriceTargets, Recommendation } from '@/types';

export function useEstimates() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const getEstimates = useCallback(async (symbol: string): Promise<Estimates | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Estimates>(`/estimates/${symbol}`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getPriceTargets = useCallback(async (symbol: string): Promise<PriceTargets | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<PriceTargets>(`/estimates/${symbol}/price-targets`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getRecommendations = useCallback(async (symbol: string): Promise<Recommendation | null> => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get<Recommendation>(`/estimates/${symbol}/recommendations`);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  return { getEstimates, getPriceTargets, getRecommendations, loading, error };
}
