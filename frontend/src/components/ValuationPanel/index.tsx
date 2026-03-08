import type { Quote, Ratios } from '@/types';
import './styles.css';

interface ValuationPanelProps {
  quote: Quote | null;
  ratios: Ratios | null;
}

function fmt(raw: number | string | undefined | null, decimals = 2): string {
  if (raw == null) return '-';
  const val = Number(raw);
  if (isNaN(val)) return '-';
  return val.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

function fmtPct(raw: number | string | undefined | null): string {
  if (raw == null) return '-';
  const val = Number(raw);
  if (isNaN(val)) return '-';
  const pct = Math.abs(val) < 1 ? val * 100 : val;
  return pct.toFixed(1) + '%';
}

function fmtLarge(raw: number | string | undefined | null): string {
  if (raw == null) return '-';
  const val = Number(raw);
  if (isNaN(val)) return '-';
  const abs = Math.abs(val);
  if (abs >= 1e12) return `$${(val / 1e12).toFixed(2)}T`;
  if (abs >= 1e9) return `$${(val / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `$${(val / 1e6).toFixed(1)}M`;
  return `$${val.toFixed(0)}`;
}

export function ValuationPanel({ quote, ratios }: ValuationPanelProps) {
  if (!ratios && !quote) return null;

  return (
    <div className="valuation-panel">
      {/* Backward Multiples */}
      <div className="valuation-panel__section">
        <h3 className="valuation-panel__title">Valuation Multiples (Trailing)</h3>
        <div className="valuation-panel__grid">
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">P/E (TTM)</span>
            <span className="valuation-panel__value">{fmt(ratios?.pe_ratio)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">EV/EBITDA</span>
            <span className="valuation-panel__value">{fmt(ratios?.ev_ebitda)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">P/B</span>
            <span className="valuation-panel__value">{fmt(ratios?.pb_ratio)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">P/S</span>
            <span className="valuation-panel__value">{fmt(ratios?.ps_ratio)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">EV/Sales</span>
            <span className="valuation-panel__value">{fmt(ratios?.ev_sales)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">Ent. Value</span>
            <span className="valuation-panel__value">{fmtLarge(ratios?.enterprise_value)}</span>
          </div>
        </div>
      </div>

      {/* Forward Multiples */}
      <div className="valuation-panel__section">
        <h3 className="valuation-panel__title">Forward Multiples</h3>
        <div className="valuation-panel__grid">
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">Forward P/E</span>
            <span className="valuation-panel__value">{fmt(ratios?.forward_pe)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">PEG Ratio</span>
            <span className="valuation-panel__value">{fmt(ratios?.peg_ratio)}</span>
          </div>
        </div>
      </div>

      {/* Profitability */}
      <div className="valuation-panel__section">
        <h3 className="valuation-panel__title">Profitability</h3>
        <div className="valuation-panel__grid">
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">Gross Margin</span>
            <span className="valuation-panel__value">{fmtPct(ratios?.gross_margin)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">Operating Margin</span>
            <span className="valuation-panel__value">{fmtPct(ratios?.operating_margin)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">Net Margin</span>
            <span className="valuation-panel__value">{fmtPct(ratios?.net_margin)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">ROE</span>
            <span className="valuation-panel__value">{fmtPct(ratios?.roe)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">ROA</span>
            <span className="valuation-panel__value">{fmtPct(ratios?.roa)}</span>
          </div>
          <div className="valuation-panel__metric">
            <span className="valuation-panel__label">D/E Ratio</span>
            <span className="valuation-panel__value">{fmt(ratios?.debt_to_equity)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ValuationPanel;
