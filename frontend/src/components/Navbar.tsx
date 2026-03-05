import { Link, useLocation } from 'react-router-dom'
import './Navbar.css'

function Navbar() {
  const location = useLocation()
  const isBatting = location.pathname.includes('/batting')
  const isPitching = location.pathname.includes('/pitching')

  return (
    <nav className="navbar">
      <div className="nav-container">
        <Link to="/" className="nav-brand">
          College Baseball Stats
        </Link>
        <div className="nav-links">
          <Link 
            to="/batting/individual" 
            className={`nav-link ${isBatting ? 'active' : ''}`}
          >
            Batting
          </Link>
          <Link 
            to="/pitching/individual" 
            className={`nav-link ${isPitching ? 'active' : ''}`}
          >
            Pitching
          </Link>
        </div>
      </div>
      
      {(isBatting || isPitching) && (
        <div className="subnav">
          <div className="nav-container">
            <div className="subnav-links">
              {isBatting && (
                <>
                  <Link 
                    to="/batting/individual" 
                    className={`subnav-link ${location.pathname === '/batting/individual' ? 'active' : ''}`}
                  >
                    Individual
                  </Link>
                  <Link 
                    to="/batting/team" 
                    className={`subnav-link ${location.pathname === '/batting/team' ? 'active' : ''}`}
                  >
                    Team
                  </Link>
                  <Link 
                    to="/batting/compare" 
                    className={`subnav-link ${location.pathname === '/batting/compare' ? 'active' : ''}`}
                  >
                    Radar
                  </Link>
                </>
              )}
              {isPitching && (
                <>
                  <Link 
                    to="/pitching/individual" 
                    className={`subnav-link ${location.pathname === '/pitching/individual' ? 'active' : ''}`}
                  >
                    Individual
                  </Link>
                  <Link 
                    to="/pitching/team" 
                    className={`subnav-link ${location.pathname === '/pitching/team' ? 'active' : ''}`}
                  >
                    Team
                  </Link>
                  <Link 
                    to="/pitching/compare" 
                    className={`subnav-link ${location.pathname === '/pitching/compare' ? 'active' : ''}`}
                  >
                    Radar
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </nav>
  )
}

export default Navbar
