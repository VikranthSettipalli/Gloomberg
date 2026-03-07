import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TickerSearch } from '@/components/TickerSearch';
import { QuoteCard } from '@/components/QuoteCard';
import { ChartPanel } from '@/components/ChartPanel';
import { useMarketData } from '@/hooks/useMarketData';
import type { Quote, Instrument } from '@/types';
import './styles.css';

export function StockDashboard() {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate = useNavigate();
  const [quote, setQuote] = useState<Quote | null>(null);
  const { getQuote, loading } = useMarketData();

  useEffect(() => {
    if (!symbol) {
      setQuote(null);
      return;
    }

    const fetchQuote = async () => {
      const data = await getQuote(symbol);
      setQuote(data);
    };

    fetchQuote();
  }, [symbol, getQuote]);

  const handleSelect = (instrument: Instrument) => {
    navigate(`/stock/${instrument.symbol}`);
  };

  return (
    <div className="stock-dashboard">
      <div className="stock-dashboard__search">
        <TickerSearch onSelect={handleSelect} />
      </div>

      {symbol ? (
        <div className="stock-dashboard__content">
          <div className="stock-dashboard__quote">
            <QuoteCard quote={quote} loading={loading} />
          </div>
          <div className="stock-dashboard__chart">
            <ChartPanel symbol={symbol} />
          </div>
        </div>
      ) : (
        <div className="stock-dashboard__empty">
          <h2>Welcome to Gloomberg</h2>
          <p>Search for a stock above to get started</p>
        </div>
      )}
    </div>
  );
}

export default StockDashboard;
