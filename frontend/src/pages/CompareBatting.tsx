import { useState, useEffect } from 'react'
import { getTeams, getYears, getTeamRoster, getPlayerBatting, PlayerProfile } from '../api'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend } from 'recharts'
import Toggle from '../components/Toggle'

// Key batting stats for radar chart
const KEY_BATTING_STATS_STD = ['AVG', 'HR', 'RBI', 'R', 'SB'];
const KEY_BATTING_STATS_ADV = ['AVG', 'OPS', 'SLG', 'OBP', 'wRC+'];

// All available batting statistics
const ALL_BATTING_STATS_STD = ['AVG', 'HR', 'RBI', 'R', 'SB', 'G', 'AB', 'PA', 'H', '1B', '2B', '3B', 'BB', 'SO', 'HBP', 'SF', 'SH', 'GDP', 'CS'];
const ALL_BATTING_STATS_ADV = ['AVG', 'OPS', 'SLG', 'OBP', 'wRC+', 'PA', 'BB%', 'K%', 'BB/K', 'ISO', 'Spd', 'BABIP', 'wSB', 'wRC', 'wRAA', 'wOBA'];

// Colors for up to 5 players
const PLAYER_COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#a4de6c'];

// Radar area calculation functions
function radarArea(r: number[]): number {
  const k = r.length;
  const theta = (2 * Math.PI) / k;
  let area = 0;

  for (let i = 0; i < k; i++) {
    const j = (i + 1) % k;
    area += r[i] * r[j];
  }

  area = 0.5 * Math.sin(theta) * area;
  return area;
}

function radarMaxArea(k: number, rMax: number): number {
  const theta = (2 * Math.PI) / k;
  const maxArea = 0.5 * k * (rMax ** 2) * Math.sin(theta);
  return maxArea;
}

function radarNormalizedArea(r: number[], rMax: number): number {
  const A = radarArea(r);
  const AMax = radarMaxArea(r.length, rMax);
  return A / AMax;
}

interface PlayerSelection {
  id: string;
  year?: number;
  team: string;
  playerName: string;
  profile?: PlayerProfile;
}

function CompareBatting() {
  const [years, setYears] = useState<number[]>([])
  const [teams, setTeams] = useState<string[]>([])
  const [isAdvanced, setIsAdvanced] = useState(true)
  const [selectedStats, setSelectedStats] = useState<string[]>(KEY_BATTING_STATS_ADV)
  const [players, setPlayers] = useState<PlayerSelection[]>([
    { id: '1', team: '', playerName: '' },
  ])
  const [availablePlayers, setAvailablePlayers] = useState<{ [key: string]: string[] }>({})
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getYears().then((availableYears) => {
      setYears(availableYears)
      // Set default year for all players
      if (availableYears.length > 0) {
        setPlayers(players.map(p => ({ ...p, year: availableYears[0] })))
      }
    }).catch((err) => setError(err.message))
  }, [])

  useEffect(() => {
    if (years.length > 0) {
      getTeams(years[0]).then(setTeams).catch((err) => setError(err.message))
    }
  }, [years])

  // Update selected stats when toggling between Standard and Advanced
  useEffect(() => {
    setSelectedStats(isAdvanced ? KEY_BATTING_STATS_ADV : KEY_BATTING_STATS_STD)
  }, [isAdvanced])

  const handleAddPlayer = () => {
    if (players.length < 5) {
      setPlayers([...players, { 
        id: Date.now().toString(), 
        year: years[0],
        team: '', 
        playerName: '' 
      }])
    }
  }

  const handleRemovePlayer = (id: string) => {
    setPlayers(players.filter(p => p.id !== id))
  }

  const handleTeamChange = async (id: string, team: string) => {
    setPlayers(players.map(p => 
      p.id === id ? { ...p, team, playerName: '' } : p
    ))
    
    if (team) {
      try {
        const year = players.find(p => p.id === id)?.year || years[0]
        const roster = await getTeamRoster(team, year)
        setAvailablePlayers({ ...availablePlayers, [id]: roster.batters })
      } catch (err: any) {
        setError(err.message)
      }
    }
  }

  const handlePlayerChange = (id: string, playerName: string) => {
    setPlayers(players.map(p => 
      p.id === id ? { ...p, playerName } : p
    ))
  }

  const handleYearChange = async (id: string, year: number) => {
    setPlayers(players.map(p => 
      p.id === id ? { ...p, year, team: '', playerName: '' } : p
    ))
    
    // Refresh teams for the new year
    try {
      const newTeams = await getTeams(year)
      setTeams(newTeams)
    } catch (err: any) {
      setError(err.message)
    }
  }

  const handleAddStat = (stat: string) => {
    if (!selectedStats.includes(stat)) {
      setSelectedStats([...selectedStats, stat])
    }
  }

  const handleRemoveStat = (stat: string) => {
    if (selectedStats.length > 3) { // Keep at least 3 stats for a meaningful radar chart
      setSelectedStats(selectedStats.filter(s => s !== stat))
    }
  }

  const handleCompare = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // Fetch both standard and advanced stats for each player
      const profilePromises = players
        .filter(p => p.playerName && p.year)
        .flatMap(p => [
          getPlayerBatting(p.playerName, false, p.year),  // Standard
          getPlayerBatting(p.playerName, true, p.year)    // Advanced
        ])
      
      const allProfiles = await Promise.all(profilePromises)
      
      // Merge standard and advanced stats for each player
      const mergedProfiles = players
        .filter(p => p.playerName && p.year)
        .map((_, idx) => {
          const stdProfile = allProfiles[idx * 2]
          const advProfile = allProfiles[idx * 2 + 1]
          
          // Combine statistics from both profiles
          const allStats = [...stdProfile.statistics]
          advProfile.statistics.forEach(advStat => {
            if (!allStats.find(s => s.name === advStat.name)) {
              allStats.push(advStat)
            }
          })
          
          return {
            ...advProfile,
            statistics: allStats
          }
        })
      
      setPlayers(players.map((p, idx) => ({
        ...p,
        profile: mergedProfiles[idx]
      })))
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message)
    } finally {
      setLoading(false)
    }
  }

  // Prepare data for radar chart
  const getComparisonData = () => {
    const playersWithProfiles = players.filter(p => p.profile)
    
    return selectedStats.map(statName => {
      const dataPoint: any = { stat: statName }
      
      playersWithProfiles.forEach((player, idx) => {
        const stat = player.profile!.statistics.find(s => s.name === statName)
        dataPoint[`player${idx}`] = stat?.percentile || 0
      })
      
      return dataPoint
    })
  }

  // Calculate normalized area for a player
  const getPlayerNormalizedArea = (playerIdx: number): number => {
    const playersWithProfiles = players.filter(p => p.profile)
    const player = playersWithProfiles[playerIdx]
    
    if (!player || !player.profile) return 0
    
    const values = selectedStats.map(statName => {
      const stat = player.profile!.statistics.find(s => s.name === statName)
      return stat?.percentile || 0
    })
    
    return radarNormalizedArea(values, 100) // rMax = 100 for percentile scale
  }

  // Get all available stats from the first player with a profile
  const getAvailableStats = (): string[] => {
    const playerWithProfile = players.find(p => p.profile)
    if (!playerWithProfile) {
      // Return all stats if no profile loaded yet
      return [...new Set([...ALL_BATTING_STATS_STD, ...ALL_BATTING_STATS_ADV])]
    }
    return playerWithProfile.profile!.statistics.map(s => s.name)
  }

  const availableStats = getAvailableStats()
  const availableStatsToAdd = availableStats.filter(stat => !selectedStats.includes(stat))

  const canAddMore = players.length < 5
  const canCompare = players.filter(p => p.playerName).length >= 1

  return (
    <div>
      <h1>Compare Individual Batting</h1>
      
      <div className="card">
        <div style={{ marginBottom: '1rem' }}>
          <Toggle 
            checked={isAdvanced} 
            onChange={setIsAdvanced}
            leftLabel="Standard"
            rightLabel="Advanced"
          />
        </div>

        {players.map((player, idx) => (
          <div key={player.id} style={{ 
            marginBottom: '1rem', 
            padding: '1rem', 
            border: '1px solid #ddd', 
            borderRadius: '4px',
            borderLeft: `4px solid ${PLAYER_COLORS[idx]}`
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <h3 style={{ margin: 0 }}>Player {idx + 1}</h3>
              {players.length > 1 && (
                <button 
                  className="button"
                  onClick={() => handleRemovePlayer(player.id)}
                  style={{ padding: '0.25rem 0.5rem', fontSize: '0.85rem' }}
                >
                  Remove
                </button>
              )}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem' }}>
              <div className="select-group">
                <label>Year</label>
                <select 
                  value={player.year || ''} 
                  onChange={(e) => handleYearChange(player.id, parseInt(e.target.value))}
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
                  value={player.team} 
                  onChange={(e) => handleTeamChange(player.id, e.target.value)}
                  disabled={!player.year}
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
                <label>Player</label>
                <select 
                  value={player.playerName} 
                  onChange={(e) => handlePlayerChange(player.id, e.target.value)}
                  disabled={!player.team}
                >
                  <option value="">Select a player...</option>
                  {(availablePlayers[player.id] || []).map((name) => (
                    <option key={name} value={name}>
                      {name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        ))}

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button 
            className="button" 
            onClick={handleAddPlayer}
            disabled={!canAddMore}
          >
            Add Player {!canAddMore && '(Max 5)'}
          </button>

          <button 
            className="button" 
            onClick={handleCompare}
            disabled={!canCompare || loading}
          >
            {loading ? 'Loading...' : 'Plot'}
          </button>
        </div>

        {/* Stat Selection UI */}
        {players.some(p => p.profile) && (
          <div style={{ marginTop: '1.5rem', paddingTop: '1.5rem', borderTop: '1px solid #ddd' }}>
            <h3 style={{ marginBottom: '0.75rem', fontSize: '1rem' }}>Selected Statistics for Radar Chart</h3>
            
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
              {selectedStats.map(stat => (
                <div 
                  key={stat}
                  style={{
                    padding: '0.4rem 0.8rem',
                    backgroundColor: '#e3f2fd',
                    border: '1px solid #2196F3',
                    borderRadius: '16px',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    fontSize: '0.9rem',
                    color: '#1565C0'
                  }}
                >
                  <span>{stat}</span>
                  {selectedStats.length > 3 && (
                    <button
                      onClick={() => handleRemoveStat(stat)}
                      style={{
                        background: 'none',
                        border: 'none',
                        cursor: 'pointer',
                        padding: '0',
                        color: '#1976D2',
                        fontWeight: 'bold',
                        fontSize: '1rem',
                        lineHeight: '1'
                      }}
                      title="Remove stat"
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}
            </div>

            {availableStatsToAdd.length > 0 && (
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 500 }}>
                  Add a statistic:
                </label>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <select 
                    onChange={(e) => {
                      if (e.target.value) {
                        handleAddStat(e.target.value)
                        e.target.value = ''
                      }
                    }}
                    style={{ flex: 1, maxWidth: '300px' }}
                  >
                    <option value="">Select a stat to add...</option>
                    {availableStatsToAdd.map(stat => (
                      <option key={stat} value={stat}>
                        {stat}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            )}
            
            {selectedStats.length === 3 && (
              <p style={{ fontSize: '0.85rem', color: '#666', marginTop: '0.5rem' }}>
                Minimum of 3 statistics required for the radar chart
              </p>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="error">
          Error: {error}
        </div>
      )}

      {players.some(p => p.profile) && (
        <div className="card" style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <h3 style={{ textAlign: 'center', marginBottom: '1rem' }}>Player Comparison</h3>
          <RadarChart 
            width={600}
            height={500}
            data={getComparisonData()}
          >
            <PolarGrid />
            <PolarAngleAxis dataKey="stat" />
            <PolarRadiusAxis 
              angle={90} 
              domain={[0, 100]} 
            />
            {players.filter(p => p.profile).map((player, idx) => (
              <Radar
                key={player.id}
                name={`${player.profile!.name} (${player.profile!.team}, ${player.year}) - Score: ${(getPlayerNormalizedArea(idx) * 100).toFixed(1)}%`}
                dataKey={`player${idx}`}
                stroke={PLAYER_COLORS[idx]}
                fill={PLAYER_COLORS[idx]}
                fillOpacity={0.3}
              />
            ))}
            <Legend />
          </RadarChart>
          <p style={{ textAlign: 'center', fontSize: '0.85rem', color: '#666', marginTop: '0.5rem' }}>
            Scale: 0-100 (National Percentile Rank)
          </p>
        </div>
      )}
    </div>
  )
}

export default CompareBatting
