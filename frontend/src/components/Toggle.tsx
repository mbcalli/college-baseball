import './Toggle.css'

interface ToggleProps {
  checked: boolean;
  onChange: (checked: boolean) => void;
  leftLabel: string;
  rightLabel: string;
}

function Toggle({ checked, onChange, leftLabel, rightLabel }: ToggleProps) {
  return (
    <div className="toggle-container">
      <span className={`toggle-label ${!checked ? 'active' : ''}`}>{leftLabel}</span>
      <label className="toggle-switch">
        <input 
          type="checkbox" 
          checked={checked} 
          onChange={(e) => onChange(e.target.checked)}
        />
        <span className="toggle-slider"></span>
      </label>
      <span className={`toggle-label ${checked ? 'active' : ''}`}>{rightLabel}</span>
    </div>
  )
}

export default Toggle
