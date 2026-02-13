import './Home.css'

function Home() {
  return (
    <div className="home">
      <h1>2026 College Baseball Statistics</h1>
      
      <div className="card">
        <p className="info-box">
          Use the navigation menu to explore individual player statistics or compare team rosters.
        </p>
      </div>

      <div className="card">
        <h2>About Percentiles</h2>
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
