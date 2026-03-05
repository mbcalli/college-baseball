import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer } from 'recharts';

interface StatBarProps {
  name: string;
  value: string;
  percentile: number;
}

function StatBar({ name, value, percentile }: StatBarProps) {
  // Ensure we have a valid number
  const safePercentile = Number(percentile) || 0;
  
  // Calculate color based on percentile (blue -> purple -> red)
  const getColor = (perc: number): string => {
    const r = Math.floor(255 * (perc / 100));
    const b = Math.floor(255 * (1 - perc / 100));
    return `rgb(${r}, 0, ${b})`;
  };

  const data = [{ name: name, percentile: safePercentile }];

  return (
    <div className="stat-bar">
      <div className="stat-bar-label">
        <span>{name}</span>
        <span>{value}</span>
      </div>
      <div style={{ width: '100%', height: '30px' }}>
        <ResponsiveContainer>
          <BarChart 
            data={data}
            layout="vertical"
            margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
          >
            <XAxis type="number" domain={[0, 100]} hide />
            <YAxis type="category" dataKey="name" hide />
            <Bar 
              dataKey="percentile" 
              fill={getColor(safePercentile)} 
              isAnimationActive={false}
              background={{ fill: '#e0e0e0' }}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div style={{ textAlign: 'right', fontSize: '0.85rem', marginTop: '2px', fontWeight: 600 }}>
        {safePercentile}th percentile
      </div>
    </div>
  );
}

export default StatBar;
