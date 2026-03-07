import { useEffect, useRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, CandlestickData, Time } from 'lightweight-charts';
import { useMarketData } from '@/hooks/useMarketData';
import type { OHLCV } from '@/types';
import './styles.css';

type Period = '1D' | '1W' | '1M' | '3M' | '1Y';

interface ChartPanelProps {
  symbol: string | null;
}

function getDateRange(period: Period): { start: string; end: string } {
  const end = new Date();
  const start = new Date();

  switch (period) {
    case '1D':
      start.setDate(end.getDate() - 1);
      break;
    case '1W':
      start.setDate(end.getDate() - 7);
      break;
    case '1M':
      start.setMonth(end.getMonth() - 1);
      break;
    case '3M':
      start.setMonth(end.getMonth() - 3);
      break;
    case '1Y':
      start.setFullYear(end.getFullYear() - 1);
      break;
  }

  return {
    start: start.toISOString().split('T')[0],
    end: end.toISOString().split('T')[0],
  };
}

function transformData(data: OHLCV[]): CandlestickData<Time>[] {
  return data.map((d) => ({
    time: d.timestamp.split('T')[0] as Time,
    open: d.open,
    high: d.high,
    low: d.low,
    close: d.close,
  }));
}

export function ChartPanel({ symbol }: ChartPanelProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const [period, setPeriod] = useState<Period>('1M');
  const [loading, setLoading] = useState(false);
  const { getHistory } = useMarketData();

  // Initialize chart
  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { color: 'transparent' },
        textColor: '#8b949e',
      },
      grid: {
        vertLines: { color: '#30363d' },
        horzLines: { color: '#30363d' },
      },
      crosshair: {
        vertLine: { color: '#58a6ff', width: 1, style: 2 },
        horzLine: { color: '#58a6ff', width: 1, style: 2 },
      },
      rightPriceScale: {
        borderColor: '#30363d',
      },
      timeScale: {
        borderColor: '#30363d',
        timeVisible: true,
      },
    });

    const series = chart.addCandlestickSeries({
      upColor: '#3fb950',
      downColor: '#f85149',
      borderUpColor: '#3fb950',
      borderDownColor: '#f85149',
      wickUpColor: '#3fb950',
      wickDownColor: '#f85149',
    });

    chartRef.current = chart;
    seriesRef.current = series;

    const handleResize = () => {
      if (chartContainerRef.current && chartRef.current) {
        chartRef.current.applyOptions({
          width: chartContainerRef.current.clientWidth,
          height: chartContainerRef.current.clientHeight,
        });
      }
    };

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, []);

  // Load data when symbol or period changes
  useEffect(() => {
    if (!symbol || !seriesRef.current) return;

    const loadData = async () => {
      setLoading(true);
      try {
        const { start, end } = getDateRange(period);
        const data = await getHistory(symbol, start, end, '1d');
        const chartData = transformData(data);

        if (seriesRef.current && chartData.length > 0) {
          seriesRef.current.setData(chartData);
          chartRef.current?.timeScale().fitContent();
        }
      } catch (err) {
        console.error('Failed to load chart data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [symbol, period, getHistory]);

  if (!symbol) {
    return (
      <div className="chart-panel chart-panel--empty">
        <p>Select a stock to view chart</p>
      </div>
    );
  }

  return (
    <div className="chart-panel">
      <div className="chart-panel__header">
        <div className="chart-panel__periods">
          {(['1D', '1W', '1M', '3M', '1Y'] as Period[]).map((p) => (
            <button
              key={p}
              className={`chart-panel__period ${period === p ? 'chart-panel__period--active' : ''}`}
              onClick={() => setPeriod(p)}
            >
              {p}
            </button>
          ))}
        </div>
        {loading && <span className="chart-panel__loading">Loading...</span>}
      </div>
      <div ref={chartContainerRef} className="chart-panel__container" />
    </div>
  );
}

export default ChartPanel;
