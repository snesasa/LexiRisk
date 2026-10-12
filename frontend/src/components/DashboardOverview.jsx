import React from 'react';
import RiskGauge from './RiskGauge';
import {
  AlertTriangle,
  AlertOctagon,
  FileCheck,
  CheckCircle2,
  TrendingUp,
  Compass,
  ArrowRight,
  ShieldCheck,
  Zap
} from 'lucide-react';

export default function DashboardOverview({ contract, onNavigateTab }) {
  if (!contract) return null;

  const stats = contract.stats || {};
  const clauses = contract.clauses || [];
  const findings = contract.findings || [];
  const scenarios = contract.scenarios || [];

  // Categorize clauses
  const categoryCounts = {};
  clauses.forEach((c) => {
    categoryCounts[c.category] = (categoryCounts[c.category] || 0) + 1;
  });

  const sortedCategories = Object.entries(categoryCounts).sort((a, b) => b[1] - a[1]);

  // Top high-risk clauses
  const topRiskyClauses = [...clauses]
    .sort((a, b) => b.risk_score - a.risk_score)
    .filter((c) => c.risk_level === 'Critical' || c.risk_level === 'High')
    .slice(0, 3);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Top Banner: Gauge + Executive Summary */}
      <div className="glass-card" style={{ display: 'flex', gap: '36px', alignItems: 'center', flexWrap: 'wrap' }}>
        <div style={{ minWidth: '220px', display: 'flex', justifyContent: 'center' }}>
          <RiskGauge score={contract.overall_risk_score} level={contract.risk_level} size={190} />
        </div>

        <div style={{ flex: 1, minWidth: '300px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--primary-light)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              EXECUTIVE AUDIT SUMMARY
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              • {new Date(contract.created_at).toLocaleDateString()}
            </span>
          </div>

          <h2 style={{ fontSize: '1.6rem', fontWeight: 800, marginBottom: '10px', letterSpacing: '-0.02em' }}>
            {contract.title}
          </h2>

          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', lineHeight: 1.6, marginBottom: '16px' }}>
            {contract.summary}
          </p>

          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button className="btn btn-primary" onClick={() => onNavigateTab('scenarios')}>
              <Compass size={16} />
              <span>Explore {scenarios.length} Dispute Scenarios</span>
              <ArrowRight size={14} />
            </button>
            <button className="btn btn-secondary" onClick={() => onNavigateTab('clauses')}>
              <FileCheck size={16} />
              <span>Inspect All {clauses.length} Clauses</span>
            </button>
          </div>
        </div>
      </div>

      {/* 4 Metric KPI Cards */}
      <div className="metrics-grid">
        <div className="metric-card" style={{ borderLeft: '4px solid var(--risk-critical)' }}>
          <div className="metric-icon-box" style={{ background: 'var(--risk-critical-bg)', color: 'var(--risk-critical)' }}>
            <AlertOctagon size={24} />
          </div>
          <div>
            <div className="metric-value" style={{ color: 'var(--risk-critical)' }}>
              {stats.critical_count || 0}
            </div>
            <div className="metric-label">Critical Risk Provisions</div>
          </div>
        </div>

        <div className="metric-card" style={{ borderLeft: '4px solid var(--risk-high)' }}>
          <div className="metric-icon-box" style={{ background: 'var(--risk-high-bg)', color: 'var(--risk-high)' }}>
            <AlertTriangle size={24} />
          </div>
          <div>
            <div className="metric-value" style={{ color: 'var(--risk-high)' }}>
              {stats.high_count || 0}
            </div>
            <div className="metric-label">High Severity Clauses</div>
          </div>
        </div>

        <div className="metric-card" style={{ borderLeft: '4px solid var(--primary)' }}>
          <div className="metric-icon-box" style={{ background: 'rgba(99, 102, 241, 0.15)', color: 'var(--primary-light)' }}>
            <Zap size={24} />
          </div>
          <div>
            <div className="metric-value" style={{ color: 'var(--primary-light)' }}>
              {scenarios.length}
            </div>
            <div className="metric-label">Future Dispute Scenarios</div>
          </div>
        </div>

        <div className="metric-card" style={{ borderLeft: '4px solid #f59e0b' }}>
          <div className="metric-icon-box" style={{ background: 'rgba(245, 158, 11, 0.15)', color: '#f59e0b' }}>
            <ShieldCheck size={24} />
          </div>
          <div>
            <div className="metric-value" style={{ color: '#f59e0b' }}>
              {findings.length}
            </div>
            <div className="metric-label">Missing Standard Protections</div>
          </div>
        </div>
      </div>

      {/* Two Column Layout: Top Flags & Category Breakdown */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px' }}>
        {/* Urgent Attention Spotlight */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle size={18} color="var(--risk-critical)" />
              <span>Highest Priority Risk Warnings</span>
            </h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Top {topRiskyClauses.length} Flagged</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {topRiskyClauses.map((c) => (
              <div
                key={c.id}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '8px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ fontWeight: 700, fontSize: '0.9rem' }}>
                    Clause {c.clause_index}: {c.category}
                  </div>
                  <span className={`risk-badge ${c.risk_level.toLowerCase()}`}>
                    {c.risk_level} ({Math.round(c.risk_score)}/100)
                  </span>
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontStyle: 'italic' }}>
                  "{c.text.length > 140 ? c.text.substring(0, 140) + '...' : c.text}"
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-primary)' }}>
                  <strong>Analysis:</strong> {c.explanation}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 41 CUAD Category Distribution */}
        <div className="glass-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <TrendingUp size={18} color="var(--accent-cyan)" />
              <span>CUAD Category Breakdown</span>
            </h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              {sortedCategories.length} Categories Identified
            </span>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', maxHeight: '280px', overflowY: 'auto' }}>
            {sortedCategories.map(([category, count]) => (
              <div
                key={category}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '6px 12px',
                  fontSize: '0.82rem'
                }}
              >
                <span style={{ fontWeight: 600 }}>{category}</span>
                <span
                  style={{
                    background: 'rgba(99, 102, 241, 0.2)',
                    color: 'var(--primary-light)',
                    borderRadius: '12px',
                    padding: '2px 8px',
                    fontSize: '0.72rem',
                    fontWeight: 700
                  }}
                >
                  {count}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
