import { useState, useEffect, useRef } from 'react';
import { useMarketData } from '@/hooks/useMarketData';
import type { Instrument } from '@/types';
import './styles.css';

interface TickerSearchProps {
  onSelect: (instrument: Instrument) => void;
  placeholder?: string;
}

export function TickerSearch({ onSelect, placeholder = 'Search stocks...' }: TickerSearchProps) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Instrument[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const { searchInstruments } = useMarketData();
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    if (query.length < 2) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      const instruments = await searchInstruments(query);
      setResults(instruments);
      setIsOpen(instruments.length > 0);
      setActiveIndex(-1);
    }, 300);

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current);
      }
    };
  }, [query, searchInstruments]);

  const handleSelect = (instrument: Instrument) => {
    setQuery('');
    setIsOpen(false);
    setResults([]);
    onSelect(instrument);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!isOpen) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((prev) => (prev < results.length - 1 ? prev + 1 : prev));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((prev) => (prev > 0 ? prev - 1 : prev));
        break;
      case 'Enter':
        e.preventDefault();
        if (activeIndex >= 0 && results[activeIndex]) {
          handleSelect(results[activeIndex]);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        setActiveIndex(-1);
        break;
    }
  };

  return (
    <div className="ticker-search">
      <input
        ref={inputRef}
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        onFocus={() => results.length > 0 && setIsOpen(true)}
        onBlur={() => setTimeout(() => setIsOpen(false), 200)}
        placeholder={placeholder}
        className="ticker-search__input"
        autoComplete="off"
        spellCheck={false}
      />
      {isOpen && results.length > 0 && (
        <ul className="ticker-search__dropdown">
          {results.map((instrument, index) => (
            <li
              key={instrument.scrip_code}
              className={`ticker-search__item ${index === activeIndex ? 'ticker-search__item--active' : ''}`}
              onClick={() => handleSelect(instrument)}
              onMouseEnter={() => setActiveIndex(index)}
            >
              <span className="ticker-search__symbol">{instrument.symbol}</span>
              <span className="ticker-search__name">{instrument.name}</span>
              <span className="ticker-search__exchange">{instrument.exchange}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default TickerSearch;
