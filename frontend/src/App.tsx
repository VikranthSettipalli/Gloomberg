import { BrowserRouter, Routes, Route } from 'react-router-dom'

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <header>
          <h1>Gloomberg</h1>
          <nav>
            <a href="/">Dashboard</a>
            <a href="/screener">Screener</a>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<div>Stock Dashboard (coming soon)</div>} />
            <Route path="/screener" element={<div>Screener (coming soon)</div>} />
            <Route path="/stock/:symbol" element={<div>Stock Detail (coming soon)</div>} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
