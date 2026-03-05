import DataStatusTerminal from '../components/DataStatusTerminal'
import './Home.css'

function Home() {
  return (
    <div className="home">
      <h1>College Baseball Stats Explorer</h1>

      <div className="card">
        <h2>Data Freshness</h2>
        <DataStatusTerminal />
      </div>

      <div className="card">
        <h2>About</h2>
        <p>
          This is a lightweight tool to explore and compare college baseball statistics.
          It provides insights into player performance using percentiles, allowing you to see how players stack up against their peers.
          Data from 2025 is taken from after the season; 2026 is updated throughout the season as stats become available.
        </p>
        
        <p>
          Created by Matt Callicott, a baseball fan and data scientist.
        </p>
      </div>

      <div className="card">
        <h2>Percentiles</h2>
        <p>
          The charts show <strong>percentiles</strong> of key statistics for each player. 
          Percentiles help understand how good a player is compared to others. For example, 
          a batting average at the 77th percentile means 77% of other players have a lower 
          batting average. <strong>Higher percentiles mean better performance.</strong>
        </p>
        
        <p>
          <strong>Note:</strong> Some statistics are better when lower (e.g., strikeout rate 
          for batters). The percentiles account for this automatically—a high percentile always 
          means better performance.
        </p>
      </div>

      <div className="card">
        <h2>Playing Time Context</h2>
        <p>
          When viewing team lineups and bullpens, you can filter by minimum plate appearances 
          (PA) or innings pitched (IP). This helps avoid inflated statistics from players with 
          limited playing time.
        </p>
      </div>

      <div className="card">
        <h2>Data Source</h2>
        <p>
          Statistics are sourced from{' '}
          <a 
            href="https://www.fangraphs.com/leaders/college" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            Fangraphs College Leaderboard
          </a>
          . Data requires a Fangraphs membership to access.
        </p>
      </div>
    </div>
  )
}

export default Home
