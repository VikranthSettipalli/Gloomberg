// Market Data Types
export interface Instrument {
  symbol: string;
  name: string;
  scrip_code: string;
  exchange: string;
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

// Fundamentals Types
export interface Financials {
  symbol: string;
  period: string;
  fiscalYear: number;
  revenue?: number;
  netIncome?: number;
  ebitda?: number;
  eps?: number;
  filingDate?: string;
}

export interface Ratios {
  symbol: string;
  peRatio?: number;
  pbRatio?: number;
  psRatio?: number;
  evEbitda?: number;
  debtToEquity?: number;
  roe?: number;
  roa?: number;
  grossMargin?: number;
  operatingMargin?: number;
  netMargin?: number;
}

// Index Types
export interface IndexData {
  symbol: string;
  name: string;
  value: number;
  change: number;
  changePercent: number;
  timestamp: string;
}

export interface Constituent {
  symbol: string;
  name: string;
  weight?: number;
  sector?: string;
}

// Estimates Types
export interface Consensus {
  mean?: number;
  median?: number;
  high?: number;
  low?: number;
  numEstimates: number;
}

export interface Estimates {
  symbol: string;
  metric: string;
  period: string;
  consensus: Consensus;
}

export interface PriceTargets {
  symbol: string;
  mean?: number;
  median?: number;
  high?: number;
  low?: number;
  numAnalysts: number;
}

export interface Recommendation {
  symbol: string;
  strongBuy: number;
  buy: number;
  hold: number;
  sell: number;
  strongSell: number;
}

// Shareholding Types
export interface Shareholding {
  symbol: string;
  quarter: string;
  year: number;
  filingDate?: string;
  promoter?: number;
  fii?: number;
  dii?: number;
  public?: number;
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
