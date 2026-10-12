import React, { useState, useEffect } from 'react';
import {
  GitCompare,
  ArrowRightLeft,
  CheckCircle,
  AlertTriangle,
  Scale,
  Sparkles,
  RefreshCw
} from 'lucide-react';

export default function SideBySideComparator({ contract, initialClause, cuadCategories }) {
  const clauses = contract ? contract.clauses || [] : [];
  const categoriesList = cuadCategories ? Object.keys(cuadCategories).sort() : [];

  const [selectedClauseIndex, setSelectedClauseIndex] = useState(
    initialClause ? initialClause.clause_index : clauses[0]?.clause_index || 1
  );
  const [clauseA, setClauseA] = useState(
    initialClause ? initialClause.text : clauses[0]?.text || ''
  );
  const [selectedCategory, setSelectedCategory] = useState(
    initialClause ? initialClause.category : clauses[0]?.category || 'Uncapped Liability'
  );

  const [comparisonMode, setComparisonMode] = useState('benchmark'); // 'benchmark' or 'custom'
  const [clauseB, setClauseB] = useState('');
  const [comparisonResult, setComparisonResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // When selected clause changes
  useEffect(() => {
    const c = clauses.find((item) => item.clause_index === Number(selectedClauseIndex));
    if (c) {
      setClauseA(c.text);
      setSelectedCategory(c.category);
    }
  }, [selectedClauseIndex, clauses]);

  // Trigger comparison against API
  const runComparison = async () => {
    setLoading(true);
    try {
      const payload = {
        clause_a: clauseA,
        clause_b: comparisonMode === 'custom' ? clauseB : null,
        category: comparisonMode === 'benchmark' ? selectedCategory : null
      };

      const res = await fetch('http://127.0.0.1:8000/api/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Comparison failed');
      const data = await res.json();
      setComparisonResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (clauseA) {
      runComparison();
    }
  }, [clauseA, selectedCategory, comparisonMode]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Top Controls Bar */}
      <div className="glass-card" style={{ padding: '16px 20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Scale size={20} color="var(--primary-light)" />
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>Side-by-Side Clause Comparator</h3>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                Benchmark contract provisions against official CUAD market precedents or compare two custom clauses.
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            {/* Quick Pick Clause from Contract */}
            {clauses.length > 0 && (
              <select
                value={selectedClauseIndex}
                onChange={(e) => setSelectedClauseIndex(Number(e.target.value))}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '8px 12px',
                  fontSize: '0.82rem',
                  fontFamily: 'var(--font-sans)',
                  cursor: 'pointer',
                  maxWidth: '240px'
                }}
              >
                {clauses.map((c) => (
                  <option key={c.id} value={c.clause_index}>
                    Clause #{c.clause_index}: {c.category}
                  </option>
                ))}
              </select>
            )}

            {/* Mode Switcher */}
            <div style={{ display: 'flex', background: 'var(--bg-surface-elevated)', borderRadius: 'var(--radius-sm)', padding: '2px' }}>
              <button
                className={`btn btn-ghost`}
                style={{
                  padding: '6px 12px',
                  fontSize: '0.78rem',
                  background: comparisonMode === 'benchmark' ? 'var(--primary)' : 'transparent',
                  color: comparisonMode === 'benchmark' ? '#fff' : 'var(--text-secondary)'
                }}
                onClick={() => setComparisonMode('benchmark')}
              >
                CUAD Precedent Benchmark
              </button>
              <button
                className={`btn btn-ghost`}
                style={{
                  padding: '6px 12px',
                  fontSize: '0.78rem',
                  background: comparisonMode === 'custom' ? 'var(--primary)' : 'transparent',
                  color: comparisonMode === 'custom' ? '#fff' : 'var(--text-secondary)'
                }}
                onClick={() => setComparisonMode('custom')}
              >
                Custom Clause Compare
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Comparison Metrics Banner */}
      {comparisonResult && (
        <div
          className="glass-card"
          style={{
            background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.8))',
            border: '1px solid rgba(99, 102, 241, 0.25)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '20px'
          }}
        >
          <div>
            <div style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              LEGAL ALIGNMENT ASSESSMENT
            </div>
            <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '4px' }}>
              {comparisonResult.comparison
                ? comparisonResult.comparison.diagnosis
                : comparisonResult.diagnosis || 'Analysis Ready'}
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--primary-light)' }}>
                {comparisonResult.comparison
                  ? `${comparisonResult.comparison.similarity_percentage}%`
                  : comparisonResult.similarity_percentage
                  ? `${comparisonResult.comparison?.similarity_percentage || comparisonResult.similarity_percentage}%`
                  : 'N/A'}
              </div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                SEMANTIC SIMILARITY
              </div>
            </div>

            <button className="btn btn-secondary btn-icon" onClick={runComparison} title="Re-run comparison">
              <RefreshCw size={16} />
            </button>
          </div>
        </div>
      )}

      {/* Split Comparison Panels */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '20px' }}>
        {/* Left Panel: Your Contract Clause */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--risk-high)', textTransform: 'uppercase' }}>
                PANEL A • YOUR CONTRACT
              </span>
              <h4 style={{ fontSize: '1rem', fontWeight: 700, marginTop: '2px' }}>
                Subject Clause Excerpt
              </h4>
            </div>
          </div>

          <textarea
            value={clauseA}
            onChange={(e) => setClauseA(e.target.value)}
            rows={10}
            style={{
              width: '100%',
              background: 'var(--bg-surface-elevated)',
              border: '1px solid var(--border-subtle)',
              borderRadius: 'var(--radius-sm)',
              padding: '12px',
              fontFamily: 'var(--font-mono)',
              fontSize: '0.85rem',
              color: 'var(--text-primary)',
              lineHeight: 1.6,
              resize: 'vertical'
            }}
          />

          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Editable: You can edit or paste any clause text to test against market standards.
          </div>
        </div>

        {/* Right Panel: Precedent or Custom Clause */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#10b981', textTransform: 'uppercase' }}>
                PANEL B • {comparisonMode === 'benchmark' ? 'CUAD MARKET BENCHMARK' : 'COUNTERPARTY CLAUSE'}
              </span>
              <h4 style={{ fontSize: '1rem', fontWeight: 700, marginTop: '2px' }}>
                {comparisonMode === 'benchmark' ? selectedCategory : 'Custom Comparison Text'}
              </h4>
            </div>

            {comparisonMode === 'benchmark' && categoriesList.length > 0 && (
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  color: 'var(--text-primary)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '6px 10px',
                  fontSize: '0.78rem',
                  fontFamily: 'var(--font-sans)',
                  cursor: 'pointer'
                }}
              >
                {categoriesList.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat}
                  </option>
                ))}
              </select>
            )}
          </div>

          {comparisonMode === 'benchmark' ? (
            <div
              className="code-box"
              style={{
                flex: 1,
                minHeight: '230px',
                borderColor: 'rgba(16, 185, 129, 0.3)',
                background: 'rgba(16, 185, 129, 0.04)',
                color: '#d1fae5'
              }}
            >
              {comparisonResult?.benchmark_text || 'Loading market precedent...'}
            </div>
          ) : (
            <textarea
              value={clauseB}
              onChange={(e) => setClauseB(e.target.value)}
              placeholder="Paste counterparty or alternate draft clause here to compare..."
              rows={10}
              style={{
                width: '100%',
                background: 'var(--bg-surface-elevated)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
                padding: '12px',
                fontFamily: 'var(--font-mono)',
                fontSize: '0.85rem',
                color: 'var(--text-primary)',
                lineHeight: 1.6,
                resize: 'vertical'
              }}
            />
          )}

          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
            Benchmark text derived from high-standard precedent language in the CUAD dataset.
          </div>
        </div>
      </div>
    </div>
  );
}
