import React, { useState } from 'react';
import {
  Search,
  Filter,
  AlertCircle,
  Copy,
  Check,
  ChevronRight,
  Sparkles,
  GitCompare,
  FileText
} from 'lucide-react';

export default function ClauseInspector({ contract, onCompareClause }) {
  if (!contract) return null;

  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRisk, setSelectedRisk] = useState('ALL');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [copiedId, setCopiedId] = useState(null);

  const clauses = contract.clauses || [];

  // Extract unique categories for filter dropdown
  const uniqueCategories = Array.from(new Set(clauses.map((c) => c.category))).sort();

  // Filter clauses
  const filteredClauses = clauses.filter((c) => {
    const matchesSearch =
      searchTerm === '' ||
      c.text.toLowerCase().includes(searchTerm.toLowerCase()) ||
      c.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (c.section_title && c.section_title.toLowerCase().includes(searchTerm.toLowerCase()));

    const matchesRisk =
      selectedRisk === 'ALL' || c.risk_level.toUpperCase() === selectedRisk;

    const matchesCategory =
      selectedCategory === 'ALL' || c.category === selectedCategory;

    return matchesSearch && matchesRisk && matchesCategory;
  });

  const handleCopyRedline = (clauseId, redlineText) => {
    navigator.clipboard.writeText(redlineText);
    setCopiedId(clauseId);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Filter and Search Bar */}
      <div className="glass-card" style={{ padding: '16px 20px' }}>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center', flexWrap: 'wrap' }}>
          {/* Search Box */}
          <div style={{ position: 'relative', flex: 1, minWidth: '260px' }}>
            <Search
              size={18}
              style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }}
            />
            <input
              type="text"
              placeholder="Search clause text, legal keywords, section headers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{
                width: '100%',
                background: 'var(--bg-surface-elevated)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '10px 14px 10px 38px',
                color: 'var(--text-primary)',
                fontFamily: 'var(--font-sans)',
                fontSize: '0.88rem'
              }}
            />
          </div>

          {/* Risk Level Filter Chips */}
          <div style={{ display: 'flex', gap: '6px' }}>
            {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((risk) => (
              <button
                key={risk}
                onClick={() => setSelectedRisk(risk)}
                style={{
                  padding: '6px 12px',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-subtle)',
                  background: selectedRisk === risk ? 'var(--primary)' : 'var(--bg-surface-elevated)',
                  color: selectedRisk === risk ? '#ffffff' : 'var(--text-secondary)',
                  fontSize: '0.78rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {risk}
              </button>
            ))}
          </div>

          {/* Category Dropdown */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            style={{
              background: 'var(--bg-surface-elevated)',
              color: 'var(--text-primary)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '8px 12px',
              fontSize: '0.82rem',
              fontFamily: 'var(--font-sans)',
              cursor: 'pointer',
              maxWidth: '220px'
            }}
          >
            <option value="ALL">All CUAD Categories ({uniqueCategories.length})</option>
            {uniqueCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Results Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0 4px' }}>
        <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
          Showing <strong>{filteredClauses.length}</strong> of {clauses.length} clauses
        </div>
      </div>

      {/* Clause Cards List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
        {filteredClauses.map((clause) => {
          const isCriticalOrHigh = clause.risk_level === 'Critical' || clause.risk_level === 'High';
          return (
            <div
              key={clause.id}
              className="glass-card"
              style={{
                borderLeft: `4px solid var(--risk-${clause.risk_level.toLowerCase()})`,
                display: 'flex',
                flexDirection: 'column',
                gap: '14px'
              }}
            >
              {/* Header Row */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '10px' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <span style={{ fontSize: '1.05rem', fontWeight: 800 }}>
                      Clause #{clause.clause_index}: {clause.category}
                    </span>
                    <span
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        color: 'var(--text-muted)',
                        background: 'var(--bg-surface-elevated)',
                        padding: '2px 8px',
                        borderRadius: '12px'
                      }}
                    >
                      {Math.round((clause.confidence || 0.85) * 100)}% Classifier Confidence
                    </span>
                  </div>

                  {clause.section_title && (
                    <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '3px' }}>
                      Section Context: <strong>{clause.section_title}</strong>
                    </div>
                  )}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <span className={`risk-badge ${clause.risk_level.toLowerCase()}`}>
                    {clause.risk_level} • {Math.round(clause.risk_score)}/100
                  </span>
                  <button
                    className="btn btn-secondary btn-icon"
                    onClick={() => onCompareClause(clause)}
                    title="Compare side-by-side with CUAD benchmark"
                  >
                    <GitCompare size={15} />
                    <span style={{ fontSize: '0.78rem' }}>Compare</span>
                  </button>
                </div>
              </div>

              {/* Exact Clause Text Excerpt */}
              <div>
                <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '6px' }}>
                  Contract Excerpt
                </div>
                <div className="code-box">
                  {clause.text}
                </div>
              </div>

              {/* Finding & Risk Factors */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div style={{ fontSize: '0.88rem', color: 'var(--text-primary)', display: 'flex', gap: '8px' }}>
                  <AlertCircle size={16} color={`var(--risk-${clause.risk_level.toLowerCase()})`} style={{ flexShrink: 0, marginTop: '2px' }} />
                  <div>
                    <strong>Legal Analysis:</strong> {clause.explanation}
                  </div>
                </div>

                {clause.risk_factors && clause.risk_factors.length > 0 && (
                  <div style={{ marginLeft: '24px', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    {clause.risk_factors.map((rf, idx) => (
                      <div key={idx} style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                        • {rf}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Possible Consequences (if high or critical) */}
              {clause.possible_consequences && clause.possible_consequences.length > 0 && (
                <div style={{ background: 'var(--bg-surface-elevated)', padding: '12px', borderRadius: 'var(--radius-sm)' }}>
                  <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '4px' }}>
                    Potential Future Consequences:
                  </div>
                  <ul style={{ paddingLeft: '18px', fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                    {clause.possible_consequences.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Proposed Redline Suggestion */}
              {clause.redline_suggestion && (
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                    <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--primary-light)', textTransform: 'uppercase' }}>
                      Recommended Protective Revision (Human Review)
                    </div>
                    <button
                      className="btn btn-ghost"
                      style={{ padding: '3px 8px', fontSize: '0.75rem' }}
                      onClick={() => handleCopyRedline(clause.id, clause.redline_suggestion)}
                    >
                      {copiedId === clause.id ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                      <span>{copiedId === clause.id ? 'Copied!' : 'Copy Redline'}</span>
                    </button>
                  </div>
                  <div className="redline-box">
                    {clause.redline_suggestion}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
