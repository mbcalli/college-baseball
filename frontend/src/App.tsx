import { Routes, Route } from 'react-router-dom'
import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import IndividualBatting from './pages/IndividualBatting'
import IndividualPitching from './pages/IndividualPitching'
import TeamBatting from './pages/TeamBatting'
import TeamPitching from './pages/TeamPitching'

function App() {
  return (
    <div className="App">
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/batting/individual" element={<IndividualBatting />} />
          <Route path="/pitching/individual" element={<IndividualPitching />} />
          <Route path="/batting/team" element={<TeamBatting />} />
          <Route path="/pitching/team" element={<TeamPitching />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
