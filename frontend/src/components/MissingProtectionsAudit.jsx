import React, { useState } from 'react';
import {
  ShieldAlert,
  AlertOctagon,
  AlertTriangle,
  Info,
  Copy,
  Check,
  PlusCircle
} from 'lucide-react';

export default function MissingProtectionsAudit({ contract }) {
  if (!contract) return null;

  const findings = contract.findings || [];
  const [copiedId, setCopiedId] = useState(null);

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      <div className="glass-card" style={{ padding: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
          <ShieldAlert size={22} color="#f59e0b" />
          <h3 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
            Missing Legal Protections & Boilerplate Audit ({findings.length})
          </h3>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
          This audit scans for standard commercial covenants that should be present to safeguard against unilateral exposure.
          Missing terms are ranked by severity with suggested boilerplate revisions.
        </p>
      </div>

      {findings.length === 0 ? (
        <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
          <div style={{ color: '#10b981', fontSize: '1.1rem', fontWeight: 700, marginBottom: '6px' }}>
            ✓ Comprehensive Protection Coverage
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.88rem' }}>
            All core baseline protections (Limitation of Liability, Termination Notice, Governing Law) were detected.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {findings.map((f) => {
            const isCritical = f.severity === 'Critical';
            const isHigh = f.severity === 'High';
            return (
              <div
                key={f.id}
                className="glass-card"
                style={{
                  borderLeft: `4px solid ${isCritical ? 'var(--risk-critical)' : isHigh ? 'var(--risk-high)' : '#eab308'}`,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '12px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    {isCritical ? (
                      <AlertOctagon size={18} color="var(--risk-critical)" />
                    ) : (
                      <AlertTriangle size={18} color="var(--risk-high)" />
                    )}
                    <h4 style={{ fontSize: '1.05rem', fontWeight: 800 }}>
                      {f.title}
                    </h4>
                  </div>
                  <span className={`risk-badge ${f.severity.toLowerCase()}`}>
                    {f.severity} Omission
                  </span>
                </div>

                <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                  {f.description}
                </div>

                {f.recommendation && (
                  <div style={{ background: 'var(--bg-surface-elevated)', padding: '14px', borderRadius: 'var(--radius-sm)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                      <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--primary-light)', textTransform: 'uppercase' }}>
                        Recommended Replacement Clause:
                      </span>
                      <button
                        className="btn btn-ghost"
                        style={{ padding: '3px 8px', fontSize: '0.75rem' }}
                        onClick={() => handleCopy(f.id, f.recommendation)}
                      >
                        {copiedId === f.id ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                        <span>{copiedId === f.id ? 'Copied' : 'Copy Clause'}</span>
                      </button>
                    </div>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.84rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                      {f.recommendation}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
