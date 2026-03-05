import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend } from 'recharts';

interface Statistic {
  name: string;
  formatted_value: string;
  percentile: number;
}

interface RadarChartProps {
  statistics: Statistic[];
  keyStats: string[];
  playerName: string;
  team: string;
}

function PlayerRadarChart({ statistics, keyStats, playerName, team }: RadarChartProps) {
  // Filter to only include key stats and format for radar chart
  const data = statistics
    .filter(stat => keyStats.includes(stat.name))
    .filter(stat => stat.percentile !== null && !isNaN(stat.percentile)) // Filter out NaN/null
    .map(stat => ({
      stat: stat.name,
      percentile: stat.percentile,
      fullMark: 100,
    }));

  if (data.length === 0) {
    return null;
  }

  return (
    <div className="card" style={{ marginTop: '1rem', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <h3 style={{ textAlign: 'center', marginBottom: '1rem' }}>{playerName} - {team}</h3>
      <RadarChart 
        width={500}
        height={400}
        data={data}
      >
        <PolarGrid />
        <PolarAngleAxis dataKey="stat" />
        <PolarRadiusAxis 
          angle={90} 
          domain={[0, 100]} 
        />
        <Radar
          name="Percentile"
          dataKey="percentile"
          stroke="#8884d8"
          fill="#8884d8"
          fillOpacity={0.6}
        />
        <Legend />
      </RadarChart>
      <p style={{ textAlign: 'center', fontSize: '0.85rem', color: '#666', marginTop: '0.5rem' }}>
        Scale: 0-100 (National Percentile Rank)
      </p>
    </div>
  );
}

export default PlayerRadarChart;
