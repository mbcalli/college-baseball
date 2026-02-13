import { Link } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">
          College Baseball Stats
        </Link>
        <div className="nav-links">
          <Link to="/batting/individual" className="nav-link">
            Individual Batting
          </Link>
          <Link to="/pitching/individual" className="nav-link">
            Individual Pitching
          </Link>
          <Link to="/batting/team" className="nav-link">
            Team Lineup
          </Link>
          <Link to="/pitching/team" className="nav-link">
            Team Bullpen
          </Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
