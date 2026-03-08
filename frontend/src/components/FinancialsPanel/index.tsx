import { useState, useEffect } from 'react';
import { useMarketData } from '@/hooks/useMarketData';
import type { IncomeStatement, BalanceSheet, CashFlowStatement } from '@/types';
import './styles.css';

interface FinancialsPanelProps {
  symbol: string;
}

type Tab = 'income' | 'balance' | 'cashflow';
type Period = 'annual' | 'quarterly';

function fmtNum(raw: number | string | undefined | null): string {
  if (raw == null) return '-';
  const val = Number(raw);
  if (isNaN(val)) return '-';
  const abs = Math.abs(val);
  if (abs >= 1e9) return `${(val / 1e9).toFixed(1)}B`;
  if (abs >= 1e6) return `${(val / 1e6).toFixed(1)}M`;
  if (abs >= 1e3) return `${(val / 1e3).toFixed(1)}K`;
  return val.toFixed(1);
}

function fmtPct(raw: number | string | undefined | null): string {
  if (raw == null) return '-';
  const val = Number(raw);
  if (isNaN(val)) return '-';
  return val.toFixed(1) + '%';
}

function fmtDate(dateStr: string | undefined): string {
  if (!dateStr) return '-';
  const d = new Date(dateStr);
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  return `${months[d.getMonth()]} ${d.getFullYear()}`;
}

interface Row {
  label: string;
  values: (string | undefined)[];
  bold?: boolean;
  indent?: boolean;
}

function DataTable({ rows, headers }: { rows: Row[]; headers: string[] }) {
  return (
    <div className="fin-table-wrapper">
      <table className="fin-table">
        <thead>
          <tr>
            <th className="fin-table__label-col"></th>
            {headers.map((h, i) => (
              <th key={i} className="fin-table__data-col">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={i} className={row.bold ? 'fin-table__row--bold' : ''}>
              <td className={`fin-table__label ${row.indent ? 'fin-table__label--indent' : ''}`}>
                {row.label}
              </td>
              {row.values.map((v, j) => (
                <td key={j} className="fin-table__value">
                  {v ?? '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function FinancialsPanel({ symbol }: FinancialsPanelProps) {
  const [tab, setTab] = useState<Tab>('income');
  const [period, setPeriod] = useState<Period>('annual');
  const [income, setIncome] = useState<IncomeStatement[]>([]);
  const [balance, setBalance] = useState<BalanceSheet[]>([]);
  const [cashflow, setCashflow] = useState<CashFlowStatement[]>([]);
  const [loading, setLoading] = useState(false);

  const { getIncomeStatements, getBalanceSheets, getCashFlowStatements } = useMarketData();

  useEffect(() => {
    if (!symbol) return;
    setLoading(true);
    const load = async () => {
      const [inc, bs, cf] = await Promise.all([
        getIncomeStatements(symbol, period),
        getBalanceSheets(symbol, period),
        getCashFlowStatements(symbol, period),
      ]);
      setIncome(inc);
      setBalance(bs);
      setCashflow(cf);
      setLoading(false);
    };
    load();
  }, [symbol, period, getIncomeStatements, getBalanceSheets, getCashFlowStatements]);

  const incomeHeaders = income.map(s => fmtDate(s.date));
  const incomeRows: Row[] = [
    { label: 'Revenue', values: income.map(s => fmtNum(s.revenue)), bold: true },
    { label: 'Cost of Revenue', values: income.map(s => fmtNum(s.cost_of_revenue)), indent: true },
    { label: 'Gross Profit', values: income.map(s => fmtNum(s.gross_profit)), bold: true },
    { label: 'Gross Margin', values: income.map(s => fmtPct(s.gross_margin)), indent: true },
    { label: 'Operating Expenses', values: income.map(s => fmtNum(s.operating_expenses)), indent: true },
    { label: 'Operating Income', values: income.map(s => fmtNum(s.operating_income)), bold: true },
    { label: 'Op. Margin', values: income.map(s => fmtPct(s.operating_margin)), indent: true },
    { label: 'EBITDA', values: income.map(s => fmtNum(s.ebitda)) },
    { label: 'Interest Expense', values: income.map(s => fmtNum(s.interest_expense)), indent: true },
    { label: 'Income Before Tax', values: income.map(s => fmtNum(s.income_before_tax)) },
    { label: 'Income Tax', values: income.map(s => fmtNum(s.income_tax)), indent: true },
    { label: 'Net Income', values: income.map(s => fmtNum(s.net_income)), bold: true },
    { label: 'Net Margin', values: income.map(s => fmtPct(s.net_margin)), indent: true },
    { label: 'EPS', values: income.map(s => s.eps != null ? Number(s.eps).toFixed(2) : '-') },
    { label: 'EPS (Diluted)', values: income.map(s => s.eps_diluted != null ? Number(s.eps_diluted).toFixed(2) : '-') },
  ];

  const balanceHeaders = balance.map(s => fmtDate(s.date));
  const balanceRows: Row[] = [
    { label: 'Cash & Equivalents', values: balance.map(s => fmtNum(s.cash_and_equivalents)) },
    { label: 'Receivables', values: balance.map(s => fmtNum(s.receivables)), indent: true },
    { label: 'Inventory', values: balance.map(s => fmtNum(s.inventory)), indent: true },
    { label: 'Total Current Assets', values: balance.map(s => fmtNum(s.total_current_assets)), bold: true },
    { label: 'PP&E', values: balance.map(s => fmtNum(s.property_plant_equipment)) },
    { label: 'Goodwill', values: balance.map(s => fmtNum(s.goodwill)), indent: true },
    { label: 'Total Assets', values: balance.map(s => fmtNum(s.total_assets)), bold: true },
    { label: 'Accounts Payable', values: balance.map(s => fmtNum(s.accounts_payable)), indent: true },
    { label: 'Short-Term Debt', values: balance.map(s => fmtNum(s.short_term_debt)), indent: true },
    { label: 'Total Current Liabilities', values: balance.map(s => fmtNum(s.total_current_liabilities)), bold: true },
    { label: 'Long-Term Debt', values: balance.map(s => fmtNum(s.long_term_debt)) },
    { label: 'Total Liabilities', values: balance.map(s => fmtNum(s.total_liabilities)), bold: true },
    { label: 'Retained Earnings', values: balance.map(s => fmtNum(s.retained_earnings)), indent: true },
    { label: 'Total Equity', values: balance.map(s => fmtNum(s.total_equity)), bold: true },
  ];

  const cfHeaders = cashflow.map(s => fmtDate(s.date));
  const cfRows: Row[] = [
    { label: 'Net Income', values: cashflow.map(s => fmtNum(s.net_income)) },
    { label: 'Depreciation & Amort.', values: cashflow.map(s => fmtNum(s.depreciation)), indent: true },
    { label: 'Change in Working Capital', values: cashflow.map(s => fmtNum(s.change_in_working_capital)), indent: true },
    { label: 'Operating Cash Flow', values: cashflow.map(s => fmtNum(s.operating_cash_flow)), bold: true },
    { label: 'Capital Expenditure', values: cashflow.map(s => fmtNum(s.capex)) },
    { label: 'Investing Cash Flow', values: cashflow.map(s => fmtNum(s.investing_cash_flow)), bold: true },
    { label: 'Debt Issued', values: cashflow.map(s => fmtNum(s.debt_issued)), indent: true },
    { label: 'Debt Repaid', values: cashflow.map(s => fmtNum(s.debt_repaid)), indent: true },
    { label: 'Dividends Paid', values: cashflow.map(s => fmtNum(s.dividends_paid)), indent: true },
    { label: 'Share Buyback', values: cashflow.map(s => fmtNum(s.share_buyback)), indent: true },
    { label: 'Financing Cash Flow', values: cashflow.map(s => fmtNum(s.financing_cash_flow)), bold: true },
    { label: 'Free Cash Flow', values: cashflow.map(s => fmtNum(s.free_cash_flow)), bold: true },
  ];

  return (
    <div className="financials-panel">
      <div className="financials-panel__header">
        <div className="financials-panel__tabs">
          {(['income', 'balance', 'cashflow'] as Tab[]).map(t => (
            <button
              key={t}
              className={`financials-panel__tab ${tab === t ? 'financials-panel__tab--active' : ''}`}
              onClick={() => setTab(t)}
            >
              {t === 'income' ? 'Income Statement' : t === 'balance' ? 'Balance Sheet' : 'Cash Flow'}
            </button>
          ))}
        </div>
        <div className="financials-panel__period-toggle">
          {(['annual', 'quarterly'] as Period[]).map(p => (
            <button
              key={p}
              className={`financials-panel__period ${period === p ? 'financials-panel__period--active' : ''}`}
              onClick={() => setPeriod(p)}
            >
              {p === 'annual' ? 'Annual' : 'Quarterly'}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="financials-panel__loading">Loading financial data...</div>
      ) : (
        <div className="financials-panel__body">
          {tab === 'income' && <DataTable rows={incomeRows} headers={incomeHeaders} />}
          {tab === 'balance' && <DataTable rows={balanceRows} headers={balanceHeaders} />}
          {tab === 'cashflow' && <DataTable rows={cfRows} headers={cfHeaders} />}
        </div>
      )}
    </div>
  );
}

export default FinancialsPanel;
