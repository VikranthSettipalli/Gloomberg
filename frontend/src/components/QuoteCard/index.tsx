import type { Quote, CompanyProfile } from '@/types';
import './styles.css';

interface QuoteCardProps {
  quote: Quote | null;
  profile: CompanyProfile | null;
  loading?: boolean;
}

function fmt(raw: number | string | undefined | null, decimals = 2): string {
  if (raw == null) return '-';
  const value = Number(raw);
  if (isNaN(value)) return '-';
  return value.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

function fmtLarge(raw: number | string | undefined | null): string {
  if (raw == null) return '-';
  const value = Number(raw);
  if (isNaN(value)) return '-';
  const abs = Math.abs(value);
  if (abs >= 1e12) return `${(value / 1e12).toFixed(2)}T`;
  if (abs >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${(value / 1e3).toFixed(1)}K`;
  return value.toFixed(0);
}

function getCurrencySymbol(currency?: string): string {
  const map: Record<string, string> = { USD: '$', INR: '\u20B9', EUR: '\u20AC', GBP: '\u00A3', JPY: '\u00A5' };
  return map[currency || 'USD'] || currency || '$';
}

export function QuoteCard({ quote, profile, loading }: QuoteCardProps) {
  if (loading && !quote) {
    return (
      <div className="quote-card quote-card--loading">
        <div className="quote-card__skeleton quote-card__skeleton--title" />
        <div className="quote-card__skeleton quote-card__skeleton--price" />
        <div className="quote-card__skeleton quote-card__skeleton--row" />
      </div>
    );
  }

  if (!quote) return null;

  const isPositive = (quote.change ?? 0) >= 0;
  const changeClass = isPositive ? 'qc-positive' : 'qc-negative';
  const curr = getCurrencySymbol(quote.currency);

  return (
    <div className="quote-card">
      <div className="quote-card__header">
        <div className="quote-card__symbol">{quote.symbol}</div>
        {profile?.sector && (
          <div className="quote-card__sector">{profile.sector} &middot; {profile.industry}</div>
        )}
      </div>
      <div className="quote-card__name">{quote.name || profile?.name || '-'}</div>

      <div className="quote-card__price-row">
        <div className="quote-card__ltp">
          <span className="quote-card__curr">{curr}</span>
          {fmt(quote.ltp)}
        </div>
        <div className={`quote-card__change ${changeClass}`}>
          {isPositive ? '+' : ''}{fmt(quote.change_percent)}%
          <span className="quote-card__change-abs">
            ({isPositive ? '+' : ''}{fmt(quote.change)})
          </span>
        </div>
      </div>

      <div className="quote-card__grid">
        <div className="quote-card__item">
          <span className="quote-card__label">Open</span>
          <span className="quote-card__value">{fmt(quote.open)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Prev Close</span>
          <span className="quote-card__value">{fmt(quote.close)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Day High</span>
          <span className="quote-card__value">{fmt(quote.high)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Day Low</span>
          <span className="quote-card__value">{fmt(quote.low)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">52W High</span>
          <span className="quote-card__value">{fmt(quote.week_52_high)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">52W Low</span>
          <span className="quote-card__value">{fmt(quote.week_52_low)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Volume</span>
          <span className="quote-card__value">{fmtLarge(quote.volume)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Avg Volume</span>
          <span className="quote-card__value">{fmtLarge(quote.avg_volume)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">Mkt Cap</span>
          <span className="quote-card__value">{fmtLarge(quote.market_cap)}</span>
        </div>
        <div className="quote-card__item">
          <span className="quote-card__label">P/E (TTM)</span>
          <span className="quote-card__value">{fmt(quote.pe_ratio)}</span>
        </div>
      </div>

      {profile?.exchange && (
        <div className="quote-card__footer">
          {profile.exchange} &middot; {profile.currency || 'USD'}
          {profile.employees && <span> &middot; {fmtLarge(profile.employees)} employees</span>}
        </div>
      )}
    </div>
  );
}

export default QuoteCard;
