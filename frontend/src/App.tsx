import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import { StockDashboard } from '@/components/StockDashboard'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header className="app-header">
          <Link to="/" className="app-logo">Gloomberg</Link>
          <nav className="app-nav">
            <Link to="/">Dashboard</Link>
            <Link to="/screener">Screener</Link>
          </nav>
        </header>
        <main className="app-main">
          <Routes>
            <Route path="/" element={<StockDashboard />} />
            <Route path="/stock/:symbol" element={<StockDashboard />} />
            <Route path="/screener" element={<div className="coming-soon">Screener (coming soon)</div>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
