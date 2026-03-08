import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TickerSearch } from '@/components/TickerSearch';
import { QuoteCard } from '@/components/QuoteCard';
import { ChartPanel } from '@/components/ChartPanel';
import { FinancialsPanel } from '@/components/FinancialsPanel';
import { ValuationPanel } from '@/components/ValuationPanel';
import { useMarketData } from '@/hooks/useMarketData';
import type { Quote, CompanyProfile, Ratios, Instrument } from '@/types';
import './styles.css';

export function StockDashboard() {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate = useNavigate();
  const [quote, setQuote] = useState<Quote | null>(null);
  const [profile, setProfile] = useState<CompanyProfile | null>(null);
  const [ratios, setRatios] = useState<Ratios | null>(null);
  const { getQuote, getProfile, getRatios, loading } = useMarketData();

  useEffect(() => {
    if (!symbol) {
      setQuote(null);
      setProfile(null);
      setRatios(null);
      return;
    }
    const decoded = decodeURIComponent(symbol);
    const fetchData = async () => {
      const [q, p, r] = await Promise.all([
        getQuote(decoded),
        getProfile(decoded),
        getRatios(decoded),
      ]);
      setQuote(q);
      setProfile(p);
      setRatios(r);
    };
    fetchData();
  }, [symbol, getQuote, getProfile, getRatios]);

  const handleSelect = (instrument: Instrument) => {
    navigate(`/stock/${encodeURIComponent(instrument.symbol)}`);
  };

  const decodedSymbol = symbol ? decodeURIComponent(symbol) : null;

  return (
    <div className="stock-dashboard">
      <div className="stock-dashboard__search">
        <TickerSearch onSelect={handleSelect} />
      </div>

      {decodedSymbol ? (
        <div className="stock-dashboard__content">
          <div className="stock-dashboard__top">
            <div className="stock-dashboard__quote-section">
              <QuoteCard quote={quote} profile={profile} loading={loading} />
            </div>
            <div className="stock-dashboard__chart-section">
              <ChartPanel symbol={decodedSymbol} />
            </div>
          </div>
          <div className="stock-dashboard__valuation">
            <ValuationPanel quote={quote} ratios={ratios} />
          </div>
          <div className="stock-dashboard__financials">
            <FinancialsPanel symbol={decodedSymbol} />
          </div>
        </div>
      ) : (
        <div className="stock-dashboard__empty">
          <div className="stock-dashboard__hero">
            <h1>GLOOMBERG</h1>
            <p>Global equity research terminal</p>
            <div className="stock-dashboard__hints">
              <span>Try: </span>
              <button onClick={() => navigate('/stock/AAPL')}>AAPL</button>
              <button onClick={() => navigate('/stock/MSFT')}>MSFT</button>
              <button onClick={() => navigate('/stock/TSLA')}>TSLA</button>
              <button onClick={() => navigate('/stock/' + encodeURIComponent('RELIANCE.NS'))}>RELIANCE.NS</button>
              <button onClick={() => navigate('/stock/GOOGL')}>GOOGL</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default StockDashboard;
