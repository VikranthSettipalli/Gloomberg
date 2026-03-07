import type { Quote } from '@/types';
import './styles.css';

interface QuoteCardProps {
  quote: Quote | null;
  loading?: boolean;
}

function formatNumber(value: number | undefined | null, decimals = 2): string {
  if (value == null) return '-';
  return value.toLocaleString('en-IN', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function formatVolume(value: number | undefined | null): string {
  if (value == null) return '-';
  if (value >= 10_000_000) return `${(value / 10_000_000).toFixed(1)}Cr`;
  if (value >= 100_000) return `${(value / 100_000).toFixed(1)}L`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1)}K`;
  return value.toString();
}

export function QuoteCard({ quote, loading }: QuoteCardProps) {
  if (loading) {
    return (
      <div className="quote-card quote-card--loading">
        <div className="quote-card__skeleton quote-card__skeleton--title" />
        <div className="quote-card__skeleton quote-card__skeleton--price" />
        <div className="quote-card__skeleton quote-card__skeleton--row" />
      </div>
    );
  }

  if (!quote) {
    return (
      <div className="quote-card quote-card--empty">
        <p>Search for a stock to see quote data</p>
      </div>
    );
  }

  const isPositive = (quote.change ?? 0) >= 0;
  const changeClass = isPositive ? 'quote-card__change--positive' : 'quote-card__change--negative';

  return (
    <div className="quote-card">
      <div className="quote-card__header">
        <div className="quote-card__symbol">{quote.symbol}</div>
        <div className="quote-card__name">{quote.name || '-'}</div>
      </div>

      <div className="quote-card__price-row">
        <div className="quote-card__ltp">
          <span className="quote-card__currency">&#8377;</span>
          {formatNumber(quote.ltp)}
        </div>
        <div className={`quote-card__change ${changeClass}`}>
          <span className="quote-card__change-percent">
            {isPositive ? '+' : ''}{formatNumber(quote.change_percent)}%
          </span>
          <span className="quote-card__change-absolute">
            {isPositive ? '+' : ''}{formatNumber(quote.change)}
          </span>
        </div>
      </div>

      <div className="quote-card__details">
        <div className="quote-card__detail">
          <span className="quote-card__label">Open</span>
          <span className="quote-card__value">{formatNumber(quote.open)}</span>
        </div>
        <div className="quote-card__detail">
          <span className="quote-card__label">High</span>
          <span className="quote-card__value">{formatNumber(quote.high)}</span>
        </div>
        <div className="quote-card__detail">
          <span className="quote-card__label">Prev Close</span>
          <span className="quote-card__value">{formatNumber(quote.close)}</span>
        </div>
        <div className="quote-card__detail">
          <span className="quote-card__label">Low</span>
          <span className="quote-card__value">{formatNumber(quote.low)}</span>
        </div>
        <div className="quote-card__detail">
          <span className="quote-card__label">Volume</span>
          <span className="quote-card__value">{formatVolume(quote.volume)}</span>
        </div>
        <div className="quote-card__detail">
          <span className="quote-card__label">Avg Vol</span>
          <span className="quote-card__value">{formatVolume(quote.avg_volume)}</span>
        </div>
      </div>
    </div>
  );
}

export default QuoteCard;
