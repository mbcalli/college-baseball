interface StatBarProps {
  name: string;
  value: string;
  percentile: number;
}

function StatBar({ name, value, percentile }: StatBarProps) {
  // Calculate color based on percentile (blue -> purple -> red)
  const getColor = (perc: number): string => {
    const r = Math.floor(255 * (perc / 100));
    const b = Math.floor(255 * (1 - perc / 100));
    return `rgb(${r}, 0, ${b})`;
  };

  return (
    <div className="stat-bar">
      <div className="stat-bar-label">
        <span>{name}</span>
        <span>{value}</span>
      </div>
      <div className="stat-bar-track">
        <div
          className="stat-bar-fill"
          style={{
            width: `${percentile}%`,
            backgroundColor: getColor(percentile),
          }}
        >
          {percentile}
        </div>
      </div>
    </div>
  );
}

export default StatBar;
