import { useState, useEffect } from 'react'
import { getTeams, getYears, getPlayerBatting, PlayerProfile } from '../api'
import StatBar from '../components/StatBar'

function TeamBatting() {
  const [years, setYears] = useState<number[]>([])
  const [selectedYear, setSelectedYear] = useState<number | undefined>(undefined)
  const [teams, setTeams] = useState<string[]>([])
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [isAdvanced, setIsAdvanced] = useState(true)
  const [minPA, setMinPA] = useState<number>(50)
  const [profiles, setProfiles] = useState<PlayerProfile[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getYears().then((availableYears) => {
      setYears(availableYears)
      if (availableYears.length > 0) {
        setSelectedYear(availableYears[0]) // Default to most recent year
      }
    }).catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    if (selectedYear) {
      getTeams(selectedYear).then(setTeams).catch((err) => setError(err.message))
    }
  }, [selectedYear])

  const handleShow = async () => {
    if (!selectedTeam || !selectedYear) return
    
    setLoading(true)
    setError(null)
    
    try {
      // Get all batters for the team
      const yearParam = selectedYear ? `?year=${selectedYear}` : ''
      const response = await fetch(`http://localhost:8000/api/teams/${selectedTeam}/roster${yearParam}`)
      const roster = await response.json()
      
      // Fetch stats for each batter
      const playerData = await Promise.all(
        roster.batters.map((name: string) => 
          getPlayerBatting(name, isAdvanced, selectedYear).catch(() => null)
        )
      )
      
      // Filter by minimum PA and sort by first stat percentile
      const filtered = playerData
        .filter((p): p is PlayerProfile => p !== null)
        .filter((p) => {
          // Find PA stat
          const paStat = p.statistics.find((s) => s.name === 'PA')
          return paStat ? paStat.value >= minPA : false
        })
        .sort((a, b) => {
          // Sort by first percentile descending
          return (b.statistics[0]?.percentile || 0) - (a.statistics[0]?.percentile || 0)
        })
      
      setProfiles(filtered)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Team Batting Lineup</h1>
      
      <div className="card">
        <div className="select-group">
          <label>Year</label>
          <select 
            value={selectedYear || ''} 
            onChange={(e) => {
              setSelectedYear(parseInt(e.target.value))
              setSelectedTeam('')
            }}
          >
            {years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </div>

        <div className="select-group">
          <label>Team</label>
          <select 
            value={selectedTeam} 
            onChange={(e) => setSelectedTeam(e.target.value)}
            disabled={!selectedYear}
          >
            <option value="">Select a team...</option>
            {teams.map((team) => (
              <option key={team} value={team}>
                {team}
              </option>
            ))}
          </select>
        </div>

        <div className="select-group">
          <label>Minimum Plate Appearances: {minPA}</label>
          <input 
            type="range" 
            min="0" 
            max="200" 
            step="10"
            value={minPA}
            onChange={(e) => setMinPA(Number(e.target.value))}
          />
        </div>

        <div className="select-group">
          <label>
            <input 
              type="checkbox" 
              checked={isAdvanced} 
              onChange={(e) => setIsAdvanced(e.target.checked)}
            />
            {' '}Advanced Stats
          </label>
        </div>

        <button 
          className="button" 
          onClick={handleShow}
          disabled={!selectedTeam || loading}
        >
          {loading ? 'Loading...' : 'Show Lineup'}
        </button>
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {profiles.length > 0 && (
        <>
          <p className="info-box">
            Showing {profiles.length} batters with {minPA}+ plate appearances
          </p>
          
          {profiles.map((profile) => (
            <div key={profile.id} className="card">
              <h3>{profile.name}</h3>
              {profile.statistics.slice(0, 5).map((stat) => (
                <StatBar
                  key={stat.name}
                  name={stat.name}
                  value={stat.formatted_value}
                  percentile={stat.percentile}
                />
              ))}
            </div>
          ))}
        </>
      )}
    </div>
  )
}

export default TeamBatting
