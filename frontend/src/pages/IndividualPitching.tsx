import { useState, useEffect } from 'react'
import { getTeams, getYears, getTeamRoster, getPlayerPitching, PlayerProfile } from '../api'
import StatBar from '../components/StatBar'

function IndividualPitching() {
  const [years, setYears] = useState<number[]>([])
  const [selectedYear, setSelectedYear] = useState<number | undefined>(undefined)
  const [teams, setTeams] = useState<string[]>([])
  const [selectedTeam, setSelectedTeam] = useState<string>('')
  const [players, setPlayers] = useState<string[]>([])
  const [selectedPlayer, setSelectedPlayer] = useState<string>('')
  const [isAdvanced, setIsAdvanced] = useState(true)
  const [profile, setProfile] = useState<PlayerProfile | null>(null)
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

  useEffect(() => {
    if (selectedTeam && selectedYear) {
      getTeamRoster(selectedTeam, selectedYear)
        .then((roster) => setPlayers(roster.pitchers))
        .catch((err) => setError(err.message))
    }
  }, [selectedTeam, selectedYear])

  const handleShow = async () => {
    if (!selectedPlayer) return
    
    setLoading(true)
    setError(null)
    
    try {
      const data = await getPlayerPitching(selectedPlayer, isAdvanced, selectedYear)
      setProfile(data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Individual Pitching Statistics</h1>
      
      <div className="card">
        <div className="select-group">
          <label>Year</label>
          <select 
            value={selectedYear || ''} 
            onChange={(e) => setSelectedYear(parseInt(e.target.value))}
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
            onChange={(e) => {
              setSelectedTeam(e.target.value)
              setSelectedPlayer('')
            }}
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
          <label>Pitcher</label>
          <select 
            value={selectedPlayer} 
            onChange={(e) => setSelectedPlayer(e.target.value)}
            disabled={!selectedTeam}
          >
            <option value="">Select a pitcher...</option>
            {players.map((player) => (
              <option key={player} value={player}>
                {player}
              </option>
            ))}
          </select>
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
          disabled={!selectedPlayer || loading}
        >
          {loading ? 'Loading...' : 'Show Statistics'}
        </button>
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {profile && (
        <div className="card">
          <h2>{profile.name} - {profile.team}</h2>
          <p className="info-box">
            National percentiles shown. 99 = 99th percentile (GREAT)
          </p>
          
          {profile.statistics.map((stat) => (
            <StatBar
              key={stat.name}
              name={stat.name}
              value={stat.formatted_value}
              percentile={stat.percentile}
            />
          ))}
        </div>
      )}
    </div>
  )
}

export default IndividualPitching
