import React, { useState } from 'react';
import {
  Compass,
  Zap,
  Clock,
  ShieldCheck,
  AlertTriangle,
  Send,
  HelpCircle,
  FileText,
  Sparkles
} from 'lucide-react';

export default function FutureScenarioExplorer({ contract }) {
  if (!contract) return null;

  const scenarios = contract.scenarios || [];

  const [hypothetical, setHypothetical] = useState('');
  const [simulationLoading, setSimulationLoading] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);

  const samplePrompts = [
    "What if our service suffers a 4-hour unscheduled downtime?",
    "What if our company gets acquired by a larger competitor?",
    "What if the client cancels the contract after 6 months?",
    "What if we launch a new product line in the counterparty's territory?"
  ];

  const handleSimulate = async (queryText) => {
    const q = queryText || hypothetical;
    if (!q.trim()) return;

    setSimulationLoading(true);
    setSimulationResult(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contract_id: contract.id,
          hypothetical_query: q
        })
      });

      if (!response.ok) throw new Error('Simulation failed');
      const data = await response.json();
      setSimulationResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setSimulationLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Interactive What-If Simulator Bar */}
      <div className="glass-card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <Sparkles size={20} color="var(--primary-light)" />
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>
            Interactive Future Dispute Simulator ("What-If" Analysis)
          </h3>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem', marginBottom: '14px' }}>
          Test hypothetical events against this contract's exact wording. The local AI will evaluate which clauses are triggered and project dispute exposure.
        </p>

        {/* Query Input */}
        <div style={{ display: 'flex', gap: '10px', marginBottom: '12px' }}>
          <input
            type="text"
            placeholder="Type a hypothetical event, e.g. 'What if we miss the project delivery deadline by 2 weeks?'"
            value={hypothetical}
            onChange={(e) => setHypothetical(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSimulate()}
            style={{
              flex: 1,
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '12px 16px',
              color: 'var(--text-primary)',
              fontFamily: 'var(--font-sans)',
              fontSize: '0.9rem'
            }}
          />
          <button
            className="btn btn-primary"
            onClick={() => handleSimulate()}
            disabled={simulationLoading}
          >
            <Send size={16} />
            <span>{simulationLoading ? 'Simulating...' : 'Simulate Scenario'}</span>
          </button>
        </div>

        {/* Quick Sample Presets */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Quick Prompts:</span>
          {samplePrompts.map((p, idx) => (
            <button
              key={idx}
              onClick={() => {
                setHypothetical(p);
                handleSimulate(p);
              }}
              style={{
                background: 'rgba(255, 255, 255, 0.04)',
                border: '1px solid var(--border-subtle)',
                borderRadius: '16px',
                padding: '4px 10px',
                fontSize: '0.75rem',
                color: 'var(--text-secondary)',
                cursor: 'pointer'
              }}
            >
              {p}
            </button>
          ))}
        </div>

        {/* Simulation Output Card */}
        {simulationResult && (
          <div
            style={{
              marginTop: '18px',
              padding: '18px',
              background: 'var(--bg-surface-elevated)',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--border-focus)',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontWeight: 800, fontSize: '1rem', color: 'var(--primary-light)' }}>
                Simulation Result: "{simulationResult.hypothetical_query}"
              </div>
              <span className={`risk-badge ${simulationResult.projected_risk.includes('Critical') ? 'critical' : simulationResult.projected_risk.includes('Moderate') ? 'high' : 'low'}`}>
                {simulationResult.projected_risk}
              </span>
            </div>

            <p style={{ fontSize: '0.88rem', color: 'var(--text-primary)', lineHeight: 1.5 }}>
              {simulationResult.outcome_summary}
            </p>

            {simulationResult.triggered_clauses && simulationResult.triggered_clauses.length > 0 && (
              <div>
                <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '6px' }}>
                  Triggered Contract Provisions:
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {simulationResult.triggered_clauses.map((tc, idx) => (
                    <div
                      key={idx}
                      style={{
                        background: 'rgba(0, 0, 0, 0.2)',
                        padding: '8px 12px',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: '0.82rem'
                      }}
                    >
                      <strong>Clause {tc.clause_index} ({tc.category}):</strong> {tc.text}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', borderTop: '1px solid var(--border-subtle)', paddingTop: '8px' }}>
              <strong>Mitigation Strategy:</strong> {simulationResult.recommended_action}
            </div>
          </div>
        )}
      </div>

      {/* Generated Contract Dispute Scenarios */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
          <Compass size={20} color="var(--accent-purple)" />
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
            Contract-Specific Dispute Scenarios ({scenarios.length})
          </h3>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(460px, 1fr))', gap: '20px' }}>
          {scenarios.map((scen) => (
            <div
              key={scen.id}
              className="glass-card"
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '14px',
                borderTop: `4px solid ${scen.impact === 'Critical' ? 'var(--risk-critical)' : 'var(--risk-high)'}`
              }}
            >
              {/* Scenario Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px' }}>
                <div>
                  <h4 style={{ fontSize: '1.1rem', fontWeight: 800, marginBottom: '4px' }}>
                    {scen.title}
                  </h4>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                    Type: <strong>{scen.dispute_type}</strong>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '6px' }}>
                  <span className={`risk-badge ${scen.probability.toLowerCase() === 'high' ? 'critical' : 'high'}`}>
                    {scen.probability} Likelihood
                  </span>
                  <span className={`risk-badge ${scen.impact.toLowerCase() === 'critical' ? 'critical' : 'high'}`}>
                    {scen.impact} Impact
                  </span>
                </div>
              </div>

              {/* Trigger Condition */}
              <div style={{ background: 'var(--bg-surface-elevated)', padding: '10px 14px', borderRadius: 'var(--radius-sm)', borderLeft: '3px solid var(--primary)' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-light)', textTransform: 'uppercase' }}>
                  Trigger Condition
                </div>
                <div style={{ fontSize: '0.84rem', color: 'var(--text-primary)', marginTop: '2px' }}>
                  {scen.trigger_event}
                </div>
              </div>

              {/* Narrative Analysis */}
              <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {scen.description}
              </div>

              {/* Escalation Timeline */}
              {scen.escalation_timeline && scen.escalation_timeline.length > 0 && (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                    <Clock size={14} />
                    <span>Projected Escalation Sequence</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {scen.escalation_timeline.map((item, idx) => (
                      <div
                        key={idx}
                        style={{
                          display: 'flex',
                          gap: '12px',
                          fontSize: '0.82rem',
                          background: 'rgba(255, 255, 255, 0.02)',
                          padding: '6px 10px',
                          borderRadius: '4px'
                        }}
                      >
                        <span style={{ fontWeight: 700, minWidth: '80px', color: 'var(--primary-light)' }}>
                          {item.period}
                        </span>
                        <span style={{ color: 'var(--text-secondary)' }}>{item.event}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Mitigations */}
              {scen.mitigations && scen.mitigations.length > 0 && (
                <div style={{ borderTop: '1px solid var(--border-subtle)', paddingTop: '10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', fontWeight: 700, color: '#10b981', textTransform: 'uppercase', marginBottom: '6px' }}>
                    <ShieldCheck size={14} />
                    <span>Recommended Mitigations</span>
                  </div>
                  <ul style={{ paddingLeft: '18px', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                    {scen.mitigations.map((m, idx) => (
                      <li key={idx} style={{ marginBottom: '4px' }}>
                        {m}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
