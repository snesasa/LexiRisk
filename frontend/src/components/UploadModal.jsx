import React, { useState, useEffect } from 'react';
import {
  X,
  Upload,
  FileText,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  FileUp,
  Cpu
} from 'lucide-react';

export default function UploadModal({ isOpen, onClose, onAnalysisComplete }) {
  if (!isOpen) return null;

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
      setErrorMsg('Please select a file (TXT, PDF, or DOCX).');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Parsing document & extracting legal clauses...');

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

      if (!res.ok) throw new Error('Analysis failed on server');
      const data = await res.json();
      onAnalysisComplete(data);
      onClose();
    } catch (err) {
      setErrorMsg(err.message || 'Error uploading file');
    } finally {
      setLoading(false);
    }
  };

  // Submit Raw Text
  const handleTextSubmit = async () => {
    if (!rawText.trim()) {
      setErrorMsg('Please paste or type contract text.');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Classifying clauses and evaluating risk with CUAD models...');

    try {
      const res = await fetch('http://127.0.0.1:8000/api/analyze-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: contractTitle.trim() || 'Custom Legal Agreement',
          text: rawText
        })
      });

      if (!res.ok) throw new Error('Analysis failed on server');
      const data = await res.json();
      onAnalysisComplete(data);
      onClose();
    } catch (err) {
      setErrorMsg(err.message || 'Error analyzing text');
    } finally {
      setLoading(false);
    }
  };

  // Load Preset Sample Contract
  const handleLoadSample = async (sampleId) => {
    setLoading(true);
    setErrorMsg('');
    setLoadingMessage('Loading preset agreement & running full CUAD AI audit...');

    try {
      const res = await fetch(`http://127.0.0.1:8000/api/samples/${sampleId}/load`, {
        method: 'POST'
      });

      if (!res.ok) throw new Error('Failed to load sample');
      const data = await res.json();
      onAnalysisComplete(data);
      onClose();
    } catch (err) {
      setErrorMsg(err.message || 'Error loading sample');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(8px)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}
    >
      <div
        className="glass-card"
        style={{
          width: '100%',
          maxWidth: '680px',
          maxHeight: '90vh',
          overflowY: 'auto',
          position: 'relative',
          padding: '28px',
          background: 'var(--bg-surface)'
        }}
      >
        {/* Close Button */}
        <button
          className="btn btn-ghost btn-icon"
          onClick={onClose}
          style={{ position: 'absolute', right: '18px', top: '18px' }}
        >
          <X size={18} />
        </button>

        <h3 style={{ fontSize: '1.35rem', fontWeight: 800, marginBottom: '6px' }}>
          Analyze Legal Agreement
        </h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.86rem', marginBottom: '20px' }}>
          Local processing ensures all contracts remain private on your machine without external cloud API transmission.
        </p>

        {/* Modal Tabs */}
        <div style={{ display: 'flex', gap: '8px', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '12px', marginBottom: '20px' }}>
          <button
            className={`tab-btn ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            <Upload size={16} />
            <span>Upload File</span>
          </button>
          <button
            className={`tab-btn ${activeTab === 'text' ? 'active' : ''}`}
            onClick={() => setActiveTab('text')}
          >
            <FileText size={16} />
            <span>Paste Text</span>
          </button>
          <button
            className={`tab-btn ${activeTab === 'samples' ? 'active' : ''}`}
            onClick={() => setActiveTab('samples')}
          >
            <Sparkles size={16} />
            <span>Preloaded Samples</span>
          </button>
        </div>

        {errorMsg && (
          <div style={{ background: 'var(--risk-critical-bg)', color: 'var(--risk-critical)', padding: '10px 14px', borderRadius: 'var(--radius-sm)', fontSize: '0.85rem', marginBottom: '16px' }}>
            {errorMsg}
          </div>
        )}

        {/* Tab 1: Upload File */}
        {activeTab === 'upload' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Title (Optional)
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
                  padding: '10px 14px',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <div
              className={`upload-dropzone ${isDragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => document.getElementById('contract-file-input').click()}
            >
              <input
                id="contract-file-input"
                type="file"
                accept=".txt,.pdf,.docx,.doc"
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />
              <FileUp size={40} color="var(--primary-light)" style={{ margin: '0 auto 12px auto' }} />
              <div style={{ fontWeight: 700, fontSize: '1rem', marginBottom: '4px' }}>
                {selectedFile ? selectedFile.name : 'Drag & drop contract file here'}
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                Supports TXT, PDF, DOCX • Fast local parsing
              </div>
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
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
                  <span>Begin AI Risk Analysis</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* Tab 2: Paste Raw Text */}
        {activeTab === 'text' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Title
              </label>
              <input
                type="text"
                placeholder="e.g. Mutual Non-Disclosure Agreement"
                value={contractTitle}
                onChange={(e) => setContractTitle(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '10px 14px',
                  color: 'var(--text-primary)',
                  fontSize: '0.88rem'
                }}
              />
            </div>

            <div>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-secondary)', display: 'block', marginBottom: '6px' }}>
                Contract Clauses & Terms
              </label>
              <textarea
                rows={10}
                placeholder="Paste the full contract text or individual sections here..."
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                style={{
                  width: '100%',
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-sm)',
                  padding: '12px',
                  color: 'var(--text-primary)',
                  fontFamily: 'var(--font-mono)',
                  fontSize: '0.84rem',
                  lineHeight: 1.5,
                  resize: 'vertical'
                }}
              />
            </div>

            <button
              className="btn btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '12px' }}
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

        {/* Tab 3: Preloaded Samples */}
        {activeTab === 'samples' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {samples.map((s) => (
              <div
                key={s.id}
                style={{
                  background: 'var(--bg-surface-elevated)',
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  padding: '16px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '16px'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 800, fontSize: '0.96rem', marginBottom: '4px' }}>
                    {s.title}
                  </div>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>
                    {s.description}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    Preview: "{s.preview.substring(0, 110)}..."
                  </div>
                </div>

                <button
                  className="btn btn-primary"
                  onClick={() => handleLoadSample(s.id)}
                  disabled={loading}
                >
                  <Sparkles size={16} />
                  <span>Load</span>
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
