import React from 'react';
import {
  ShieldAlert,
  Sun,
  Moon,
  Award,
  PlusCircle,
  FileText
} from 'lucide-react';

export default function Navbar({
  contract,
  contractsList,
  onSelectContract,
  onNewContract,
  onOpenAccuracy,
  theme,
  onToggleTheme
}) {
  return (
    <header className="top-navbar">
      <div className="brand-section">
        <div className="brand-icon-wrapper">
          <ShieldAlert size={20} />
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span className="brand-title">LexiRisk</span>
            <span className="brand-tag">Legal Intelligence</span>
          </div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            Contract Clause Risk Analyzer & Future Scenario Detection
          </div>
        </div>
      </div>

      <div className="nav-actions">
        {/* Model Accuracy Specs Modal Trigger */}
        <button
          className="btn btn-ghost"
          onClick={onOpenAccuracy}
          style={{ fontSize: '0.82rem', gap: '6px' }}
        >
          <Award size={15} color="var(--primary)" />
          <span>Model Accuracy (88.4%)</span>
        </button>

        {/* If contract is active, show Quick Switcher or New Upload */}
        {contract && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {contractsList && contractsList.length > 1 && (
              <select
                value={contract.id}
                onChange={(e) => onSelectContract(e.target.value)}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '7px 12px',
                  fontSize: '0.82rem',
                  fontFamily: 'var(--font-sans)',
                  cursor: 'pointer',
                  maxWidth: '220px'
                }}
              >
                {contractsList.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.title.length > 24 ? c.title.substring(0, 24) + '...' : c.title}
                  </option>
                ))}
              </select>
            )}

            <button
              className="btn btn-secondary"
              onClick={onNewContract}
              style={{ fontSize: '0.82rem', padding: '7px 14px' }}
            >
              <PlusCircle size={15} />
              <span>Analyze Another Contract</span>
            </button>
          </div>
        )}

        {/* Theme Toggle */}
        <button
          className="btn btn-ghost btn-icon"
          onClick={onToggleTheme}
          title="Toggle Dark/Light Mode"
          aria-label="Toggle Theme"
        >
          {theme === 'dark' ? <Sun size={17} /> : <Moon size={17} />}
        </button>
      </div>
    </header>
  );
}
