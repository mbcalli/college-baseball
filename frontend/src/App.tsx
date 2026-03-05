import { Routes, Route } from 'react-router-dom'
import './App.css'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import IndividualBatting from './pages/IndividualBatting'
import IndividualPitching from './pages/IndividualPitching'
import TeamBatting from './pages/TeamBatting'
import TeamPitching from './pages/TeamPitching'
import CompareBatting from './pages/CompareBatting'
import ComparePitching from './pages/ComparePitching'

function App() {
  return (
    <div className="App">
      <Navbar />
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/batting/individual" element={<IndividualBatting />} />
          <Route path="/batting/compare" element={<CompareBatting />} />
          <Route path="/pitching/individual" element={<IndividualPitching />} />
          <Route path="/pitching/compare" element={<ComparePitching />} />
          <Route path="/batting/team" element={<TeamBatting />} />
          <Route path="/pitching/team" element={<TeamPitching />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
