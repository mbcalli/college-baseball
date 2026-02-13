import { useState, useEffect } from 'react'
import { getTeams, getYears, getPlayerPitching, PlayerProfile } from '../api'
import StatBar from '../components/StatBar'

function TeamPitching() {
  const [years, setYears] = useState<number[]>([])
  const [selectedYear, setSelectedYear] = useState<number | undefined>(undefined)
  const [teams, setTeams] = useState<string[]>([])
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [isAdvanced, setIsAdvanced] = useState(true)
  const [minIP, setMinIP] = useState<number>(20)
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
      // Get all pitchers for the team
      const yearParam = selectedYear ? `?year=${selectedYear}` : ''
      const response = await fetch(`http://localhost:8000/api/teams/${selectedTeam}/roster${yearParam}`)
      const roster = await response.json()
      
      // Fetch stats for each pitcher
      const playerData = await Promise.all(
        roster.pitchers.map((name: string) => 
          getPlayerPitching(name, isAdvanced, selectedYear).catch(() => null)
        )
      )
      
      // Filter by minimum IP and sort by first stat percentile
      const filtered = playerData
        .filter((p): p is PlayerProfile => p !== null)
        .filter((p) => {
          // Find IP stat
          const ipStat = p.statistics.find((s) => s.name === 'IP')
          return ipStat ? ipStat.value >= minIP : false
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
      <h1>Team Pitching Staff</h1>
      
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
          <label>Minimum Innings Pitched: {minIP}</label>
          <input 
            type="range" 
            min="0" 
            max="100" 
            step="5"
            value={minIP}
            onChange={(e) => setMinIP(Number(e.target.value))}
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
          {loading ? 'Loading...' : 'Show Bullpen'}
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
            Showing {profiles.length} pitchers with {minIP}+ innings pitched
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

export default TeamPitching
