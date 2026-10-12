import React, { useState, useEffect } from 'react';
import {
  Upload,
  FileText,
  Sparkles,
  FileUp,
  Cpu,
  Shield,
  ArrowRight,
  FileCheck,
  Scale,
  CheckCircle2
} from 'lucide-react';

export default function ContractIngestionHero({ onContractLoaded, onOpenAccuracy }) {
  const [activeTab, setActiveTab] = useState('upload'); // 'upload', 'text', 'samples'
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [contractTitle, setContractTitle] = useState('');
  const [rawText, setRawText] = useState('');
  const [samples, setSamples] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch sample contracts
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/samples')
      .then((res) => res.json())
      .then((data) => setSamples(data))
      .catch((err) => console.error('Failed to load samples:', err));
  }, []);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      if (!contractTitle) {
        setContractTitle(file.name.replace(/\.[^/.]+$/, '').replace(/_/g, ' '));
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      if (!contractTitle) {
        setContractTitle(file.name.replace(/\.[^/.]+$/, '').replace(/_/g, ' '));
      }
    }
  };

  // Submit File Upload
  const handleFileUpload = async () => {
    if (!selectedFile) {
      setErrorMsg('Please select a file (.txt, .pdf, or .docx).');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Parsing document & extracting clauses...');

    const formData = new FormData();
    formData.append('file', selectedFile);
    if (contractTitle) {
      formData.append('title', contractTitle);
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/api/upload', {
        method: 'POST',
        body: formData
      });

      if (!res.ok) throw new Error('Document analysis failed');
      const data = await res.json();
      onContractLoaded(data);
    } catch (err) {
      setErrorMsg(err.message || 'Error processing document');
    } finally {
      setLoading(false);
    }
  };

  // Submit Raw Text
  const handleTextSubmit = async () => {
    if (!rawText.trim()) {
      setErrorMsg('Please enter or paste contract clauses.');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Classifying against 41 CUAD categories & auditing risk...');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: contractTitle.trim() || 'Custom Commercial Agreement',
          text: rawText
        })
      });

      if (!res.ok) throw new Error('Analysis failed on server');
      const data = await res.json();
      onContractLoaded(data);
    } catch (err) {
      setErrorMsg(err.message || 'Error analyzing contract text');
    } finally {
      setLoading(false);
    }
  };

  // Load Preset Sample Contract
  const handleLoadSample = async (sampleId) => {
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Loading reference agreement & running CUAD audit...');

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/samples/${sampleId}/load`, {
        method: 'POST'
      });

      if (!res.ok) throw new Error('Failed to load sample');
      const data = await res.json();
      onContractLoaded(data);
    } catch (err) {
      setErrorMsg(err.message || 'Error loading sample');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '960px', margin: '40px auto', padding: '0 20px' }}>
      {/* Hero Header */}
      <div style={{ textAlign: 'center', marginBottom: '36px' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '4px 12px', borderRadius: '20px', background: 'var(--bg-surface-elevated)', border: '1px solid var(--border-subtle)', marginBottom: '16px' }}>
          <Shield size={14} color="var(--primary)" />
          <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)' }}>
            100% Local Inference • Zero External Cloud Transmission
          </span>
        </div>

        <h1 style={{ fontSize: '2.4rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: '12px', color: 'var(--text-primary)' }}>
          Contract Clause Risk Analyzer & Future Scenario Detection
        </h1>

        <p style={{ fontSize: '1.02rem', color: 'var(--text-secondary)', maxWidth: '680px', margin: '0 auto', lineHeight: 1.6 }}>
          Identify potentially risky, ambiguous, or incomplete clauses in legal agreements.
          Combines calibrated Transformer models on the 41 CUAD categories with deterministic risk heuristics and dispute simulation.
        </p>

        <div style={{ marginTop: '14px' }}>
          <button
            className="btn btn-ghost"
            style={{ fontSize: '0.82rem', color: 'var(--primary)', textDecoration: 'underline' }}
            onClick={onOpenAccuracy}
          >
            View Model Accuracy & CUAD Benchmark Specs (88.4% Top-1 Accuracy)
          </button>
        </div>
      </div>

      {/* Main Ingestion Card */}
      <div className="glass-card" style={{ padding: '32px' }}>
        {/* Ingestion Tabs */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '14px', marginBottom: '24px' }}>
          <button
            className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            <Upload size={16} />
            <span>Upload Document</span>
          </button>
          <button
            className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => setActiveTab('text')}
          >
            <FileText size={16} />
            <span>Paste Contract Text</span>
          </button>
          <button
            className={`tab-btn ${activeTab === 'samples' ? 'active' : ''}`}
            onClick={() => setActiveTab('samples')}
          >
            <Scale size={16} />
            <span>Reference CUAD Benchmark Agreements</span>
          </button>
        </div>

        {errorMsg && (
          <div style={{ background: 'var(--risk-critical-bg)', color: 'var(--risk-critical)', padding: '12px 16px', borderRadius: 'var(--radius-sm)', fontSize: '0.86rem', marginBottom: '18px', border: '1px solid var(--risk-critical-border)' }}>
            {errorMsg}
          </div>
        )}

        {/* Tab 1: Upload File */}
        {activeTab === 'upload' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Title / Reference Name (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g. Master Services Agreement 2026"
                value={contractTitle}
                onChange={(e) => setContractTitle(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px 16px',
                  color: 'var(--text-primary)',
                  fontSize: '0.9rem'
                }}
              />
            </div>

            <div
              className={`upload-dropzone ${isDragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('hero-file-input').click()}
            >
              <input
                id="hero-file-input"
                type="file"
                accept=".txt,.pdf,.docx,.doc"
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />
              <FileUp size={44} color="var(--primary)" style={{ margin: '0 auto 12px auto' }} />
              <div style={{ fontWeight: 700, fontSize: '1.05rem', marginBottom: '4px' }}>
                {selectedFile ? selectedFile.name : 'Select or drag & drop contract file'}
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                Supports PDF, DOCX, and TXT • Segmented locally
              </div>
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '0.96rem' }}
              onClick={handleFileUpload}
              disabled={loading || !selectedFile}
            >
              {loading ? (
                <>
                  <Cpu className="animate-spin" size={18} />
                  <span>{loadingMessage}</span>
                </>
              ) : (
                <>
                  <Upload size={18} />
                  <span>Analyze Contract for Risk & Future Scenarios</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Tab 2: Paste Raw Text */}
        {activeTab === 'text' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Title
              </label>
              <input
                type="text"
                placeholder="e.g. Software License & Services Agreement"
                value={contractTitle}
                onChange={(e) => setContractTitle(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px 16px',
                  color: 'var(--text-primary)',
                  fontSize: '0.9rem'
                }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Text (Paste full agreement or sections)
              </label>
              <textarea
                rows={12}
                placeholder="Paste contract clauses here..."
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '14px',
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.84rem',
                  lineHeight: 1.6,
                  resize: 'vertical'
                }}
              />
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '0.96rem' }}
              onClick={handleTextSubmit}
              disabled={loading || !rawText.trim()}
            >
              {loading ? (
                <>
                  <Cpu className="animate-spin" size={18} />
                  <span>{loadingMessage}</span>
                </>
              ) : (
                <>
                  <Upload size={18} />
                  <span>Analyze Contract Text</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Tab 3: Preloaded Reference Samples */}
        {activeTab === 'samples' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
              Select a benchmark legal agreement drawn from the CUAD dataset repository to test the classification and scenario simulation immediately:
            </p>
            {samples.map((s) => (
              <div
                key={s.id}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '18px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '20px'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 800, fontSize: '1rem', marginBottom: '4px', color: 'var(--text-primary)' }}>
                    {s.title}
                  </div>
                  <div style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', marginBottom: '8px', lineHeight: 1.5 }}>
                    {s.description}
                  </div>
                  <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    Preview: "{s.preview.substring(0, 120)}..."
                  </div>
                </div>

                <button
                  className="btn btn-secondary"
                  onClick={() => handleLoadSample(s.id)}
                  disabled={loading}
                  style={{ whiteSpace: 'nowrap' }}
                >
                  <span>Load & Analyze</span>
                  <ArrowRight size={14} />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
