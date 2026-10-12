import React from 'react';

export default function RiskGauge({ score = 0, level = 'Low', size = 180 }) {
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  // Arc over 270 degrees
  const angleRange = 270;
  const dashoffset = circumference - (score / 100) * ((angleRange / 360) * circumference);

  const getColor = () => {
    if (score >= 75) return '#ef4444';
    if (score >= 50) return '#f97316';
    if (score >= 30) return '#eab308';
    return '#10b981';
  };

  const color = getColor();

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative' }}>
      <svg width={size} height={size} style={{ transform: 'rotate(135deg)', overflow: 'visible' }}>
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          strokeDasharray={`${(angleRange / 360) * circumference} ${circumference}`}
          strokeLinecap="round"
        />
        {/* Animated value arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={`${(angleRange / 360) * circumference} ${circumference}`}
          strokeDashoffset={dashoffset}
          strokeLinecap="round"
          style={{
            transition: 'stroke-dashoffset 1.2s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.5s ease',
            filter: `drop-shadow(0 0 8px ${color}66)`
          }}
        />
      </svg>
      {/* Centered Score Display */}
      <div style={{
        position: 'absolute',
        top: '46%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        textAlign: 'center'
      }}>
        <div style={{
          fontSize: '2.4rem',
          fontWeight: 800,
          lineHeight: 1,
          color: 'var(--text-primary)',
          letterSpacing: '-0.03em'
        }}>
          {Math.round(score)}
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
          OUT OF 100
        </div>
      </div>
      {/* Tier Label */}
      <div style={{ marginTop: '8px', textAlign: 'center' }}>
        <span className={`risk-badge ${level.toLowerCase()}`} style={{ fontSize: '0.85rem', padding: '6px 14px' }}>
          {level} Risk Profile
        </span>
      </div>
    </div>
  );
}
