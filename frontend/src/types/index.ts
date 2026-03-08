// Market Data Types
export interface Instrument {
  symbol: string;
  name: string;
  scrip_code?: string;
  exchange: string;
  type?: string;
}

export interface Quote {
  symbol: string;
  name?: string;
  ltp: number;
  change?: number;
  change_percent?: number;
  open?: number;
  high?: number;
  low?: number;
  close?: number;
  volume?: number;
  avg_volume?: number;
  bid?: number;
  ask?: number;
  timestamp: string;
  market_cap?: number;
  pe_ratio?: number;
  week_52_high?: number;
  week_52_low?: number;
  currency?: string;
}

export interface OHLCV {
  symbol: string;
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

// Company Profile
export interface CompanyProfile {
  symbol: string;
  name: string;
  sector?: string;
  industry?: string;
  country?: string;
  exchange?: string;
  currency?: string;
  market_cap?: number;
  employees?: number;
  description?: string;
  website?: string;
}

// Financial Statements
export interface IncomeStatement {
  symbol: string;
  period: string;
  date: string;
  fiscal_year?: number;
  revenue?: number;
  cost_of_revenue?: number;
  gross_profit?: number;
  operating_expenses?: number;
  operating_income?: number;
  ebitda?: number;
  interest_expense?: number;
  income_before_tax?: number;
  income_tax?: number;
  net_income?: number;
  eps?: number;
  eps_diluted?: number;
  shares_outstanding?: number;
  gross_margin?: number;
  operating_margin?: number;
  net_margin?: number;
}

export interface BalanceSheet {
  symbol: string;
  period: string;
  date: string;
  fiscal_year?: number;
  cash_and_equivalents?: number;
  short_term_investments?: number;
  receivables?: number;
  inventory?: number;
  total_current_assets?: number;
  property_plant_equipment?: number;
  goodwill?: number;
  intangible_assets?: number;
  total_assets?: number;
  accounts_payable?: number;
  short_term_debt?: number;
  total_current_liabilities?: number;
  long_term_debt?: number;
  total_liabilities?: number;
  total_equity?: number;
  retained_earnings?: number;
}

export interface CashFlowStatement {
  symbol: string;
  period: string;
  date: string;
  fiscal_year?: number;
  net_income?: number;
  depreciation?: number;
  change_in_working_capital?: number;
  operating_cash_flow?: number;
  capex?: number;
  acquisitions?: number;
  investing_cash_flow?: number;
  debt_issued?: number;
  debt_repaid?: number;
  dividends_paid?: number;
  share_buyback?: number;
  financing_cash_flow?: number;
  free_cash_flow?: number;
}

// Ratios & Multiples
export interface Ratios {
  symbol: string;
  pe_ratio?: number;
  pb_ratio?: number;
  ps_ratio?: number;
  ev_ebitda?: number;
  ev_sales?: number;
  forward_pe?: number;
  forward_ev_ebitda?: number;
  peg_ratio?: number;
  roe?: number;
  roic?: number;
  roa?: number;
  gross_margin?: number;
  operating_margin?: number;
  net_margin?: number;
  debt_to_equity?: number;
  current_ratio?: number;
  revenue_per_share?: number;
  book_value_per_share?: number;
  enterprise_value?: number;
  market_cap?: number;
}

// Screener Types
export interface ScreenerFilter {
  field: string;
  operator: string;
  value: unknown;
}

export interface ScreenerQuery {
  filters: ScreenerFilter[];
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}

export interface ScreenerResult {
  symbol: string;
  name?: string;
  data: Record<string, unknown>;
}
