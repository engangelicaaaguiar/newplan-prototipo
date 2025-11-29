import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Dashboard } from './components/Dashboard'
import { Importacao } from './components/Importacao'
import { Questionario } from './components/Questionario'
import { AnaliseRisco } from './components/AnaliseRisco'
import { Documentos } from './components/Documentos'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/importacao" element={<Importacao />} />
        <Route path="/questionarios" element={<Questionario />} />
        <Route path="/analise-risco" element={<AnaliseRisco />} />
        <Route path="/documentos" element={<Documentos />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
