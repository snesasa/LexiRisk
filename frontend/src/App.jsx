import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ContractIngestionHero from './components/ContractIngestionHero';
import DashboardOverview from './components/DashboardOverview';
import ClauseInspector from './components/ClauseInspector';
import FutureScenarioExplorer from './components/FutureScenarioExplorer';
import SideBySideComparator from './components/SideBySideComparator';
import MissingProtectionsAudit from './components/MissingProtectionsAudit';
import ModelAccuracyModal from './components/ModelAccuracyModal';

import {
  LayoutDashboard,
  FileSearch,
  Compass,
  GitCompare,
  ShieldAlert,
  AlertCircle,
  Download,
  ChevronDown,
  FileText,
  BookOpen,
  Sparkles,
  PlusCircle
} from 'lucide-react';

export default function App() {
  const [theme, setTheme] = useState('dark');
  const [activeTab, setActiveTab] = useState('overview'); // overview, clauses, scenarios, compare, missing
  const [contractsList, setContractsList] = useState([]);
  const [currentContract, setCurrentContract] = useState(null);
  const [comparatorClause, setComparatorClause] = useState(null);
  const [cuadCategories, setCuadCategories] = useState({});
  const [loading, setLoading] = useState(false);
  const [showExportMenu, setShowExportMenu] = useState(false);
  const [isAccuracyModalOpen, setIsAccuracyModalOpen] = useState(false);

  // Toggle theme
  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Load contracts and CUAD categories on mount
  useEffect(() => {
    async function initData() {
      try {
        const [contractsRes, categoriesRes] = await Promise.all([
          fetch('http://127.0.0.1:8000/api/contracts'),
          fetch('http://127.0.0.1:8000/api/cuad/categories')
        ]);

        const contracts = await contractsRes.json();
        const categories = await categoriesRes.json();

        setContractsList(contracts);
        setCuadCategories(categories);

        // NOTE: We intentionally DO NOT auto-load any contract on start,
        // so the user starts on the clean, professional Ingestion Workspace!
      } catch (err) {
        console.error('Initialization error:', err);
      }
    }
    initData();
  }, []);

  const loadContractDetails = async (contractId) => {
    setLoading(true);
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/contracts/${contractId}`);
      if (res.ok) {
        const data = await res.json();
        setCurrentContract(data);
        setActiveTab('overview');
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleContractLoaded = (newContract) => {
    setCurrentContract(newContract);
    setContractsList((prev) => [
      {
        id: newContract.id,
        title: newContract.title,
        filename: newContract.filename,
        file_type: newContract.file_type,
        overall_risk_score: newContract.overall_risk_score,
        risk_level: newContract.risk_level,
        summary: newContract.summary,
        created_at: newContract.created_at
      },
      ...prev.filter((c) => c.id !== newContract.id)
    ]);
    setActiveTab('overview');
  };

  const handleOpenComparatorForClause = (clause) => {
    setComparatorClause(clause);
    setActiveTab('compare');
  };

  const handleExport = (format) => {
    if (!currentContract) return;
    const url = `http://127.0.0.1:8000/api/contracts/${currentContract.id}/export/${format}`;
    window.open(url, '_blank');
  };

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <Navbar
        contract={currentContract}
        contractsList={contractsList}
        onSelectContract={(id) => loadContractDetails(id)}
        onNewContract={() => setCurrentContract(null)}
        onOpenAccuracy={() => setIsAccuracyModalOpen(true)}
        theme={theme}
        onToggleTheme={toggleTheme}
      />

      {/* When NO contract is active: Show Clean Ingestion Landing */}
      {!currentContract && (
        <ContractIngestionHero
          onContractLoaded={handleContractLoaded}
          onOpenAccuracy={() => setIsAccuracyModalOpen(true)}
        />
      )}

      {/* When a contract IS active: Show Active Analysis Workspace */}
      {currentContract && (
        <>
          {/* Contract Action & Export Bar - ONLY visible after uploading */}
          <div className="contract-header-bar">
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800 }}>
                  {currentContract.title}
                </h2>
                <span className={`risk-badge ${currentContract.risk_level.toLowerCase()}`}>
                  {currentContract.risk_level} Risk • {Math.round(currentContract.overall_risk_score)}/100
                </span>
              </div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                Source: {currentContract.filename || 'Direct Text Input'} • Audited: {new Date(currentContract.created_at).toLocaleDateString()}
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              {/* Export Report Dropdown */}
              <div style={{ position: 'relative' }}>
                <button
                  className="btn btn-primary"
                  onClick={() => setShowExportMenu(!showExportMenu)}
                  id="btn-export-report"
                >
                  <Download size={15} />
                  <span>Export Audit Report</span>
                  <ChevronDown size={14} />
                </button>

                {showExportMenu && (
                  <div
                    style={{
                      position: 'absolute',
                      right: 0,
                      top: '115%',
                      background: 'var(--bg-surface-elevated)',
                      border: '1px solid var(--border-subtle)',
                      borderRadius: 'var(--radius-sm)',
                      boxShadow: 'var(--shadow-lg)',
                      padding: '6px',
                      zIndex: 200,
                      minWidth: '200px'
                    }}
                  >
                    <button
                      className="btn btn-ghost"
                      style={{ width: '100%', justifyContent: 'flex-start' }}
                      onClick={() => {
                        handleExport('html');
                        setShowExportMenu(false);
                      }}
                    >
                      <FileText size={15} />
                      <span>Printable HTML Report</span>
                    </button>
                    <button
                      className="btn btn-ghost"
                      style={{ width: '100%', justifyContent: 'flex-start' }}
                      onClick={() => {
                        handleExport('markdown');
                        setShowExportMenu(false);
                      }}
                    >
                      <BookOpen size={15} />
                      <span>Markdown Summary (.md)</span>
                    </button>
                    <button
                      className="btn btn-ghost"
                      style={{ width: '100%', justifyContent: 'flex-start' }}
                      onClick={() => {
                        handleExport('json');
                        setShowExportMenu(false);
                      }}
                    >
                      <Sparkles size={15} />
                      <span>Raw Audit Data (JSON)</span>
                    </button>
                  </div>
                )}
              </div>

              <button
                className="btn btn-secondary"
                onClick={() => setCurrentContract(null)}
              >
                <PlusCircle size={15} />
                <span>Upload New</span>
              </button>
            </div>
          </div>

          {/* Main Tab Navigation */}
          <nav className="tabs-header" aria-label="Main Navigation">
            <button
              className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
              onClick={() => setActiveTab('overview')}
              id="tab-overview"
            >
              <LayoutDashboard size={16} />
              <span>Executive Dashboard</span>
            </button>

            <button
              className={`tab-btn ${activeTab === 'clauses' ? 'active' : ''}`}
              onClick={() => setActiveTab('clauses')}
              id="tab-clauses"
            >
              <FileSearch size={16} />
              <span>Clause Inspector ({currentContract.clauses?.length || 0})</span>
            </button>

            <button
              className={`tab-btn ${activeTab === 'scenarios' ? 'active' : ''}`}
              onClick={() => setActiveTab('scenarios')}
              id="tab-scenarios"
            >
              <Compass size={16} />
              <span>Future Scenarios ({currentContract.scenarios?.length || 0})</span>
            </button>

            <button
              className={`tab-btn ${activeTab === 'compare' ? 'active' : ''}`}
              onClick={() => setActiveTab('compare')}
              id="tab-compare"
            >
              <GitCompare size={16} />
              <span>Side-by-Side Comparator</span>
            </button>

            <button
              className={`tab-btn ${activeTab === 'missing' ? 'active' : ''}`}
              onClick={() => setActiveTab('missing')}
              id="tab-missing"
            >
              <ShieldAlert size={16} />
              <span>Missing Protections ({currentContract.findings?.length || 0})</span>
            </button>
          </nav>

          {/* Workspace Views */}
          <main className="main-content">
            {loading ? (
              <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-secondary)' }}>
                <p>Loading contract analysis...</p>
              </div>
            ) : (
              <>
                {activeTab === 'overview' && (
                  <DashboardOverview
                    contract={currentContract}
                    onNavigateTab={(tab) => setActiveTab(tab)}
                  />
                )}

                {activeTab === 'clauses' && (
                  <ClauseInspector
                    contract={currentContract}
                    onCompareClause={handleOpenComparatorForClause}
                  />
                )}

                {activeTab === 'scenarios' && (
                  <FutureScenarioExplorer
                    contract={currentContract}
                  />
                )}

                {activeTab === 'compare' && (
                  <SideBySideComparator
                    contract={currentContract}
                    initialClause={comparatorClause}
                    cuadCategories={cuadCategories}
                  />
                )}

                {activeTab === 'missing' && (
                  <MissingProtectionsAudit
                    contract={currentContract}
                  />
                )}
              </>
            )}

            <footer className="legal-disclaimer">
              <AlertCircle size={16} style={{ flexShrink: 0, color: 'var(--text-muted)' }} />
              <div>
                <strong>Legal Practice Disclaimer:</strong> LexiRisk AI is an automated decision-support system utilizing the CUAD legal dataset to highlight contractual provisions and model dispute scenarios. It does not provide formal legal counsel or guarantee legal enforceability in judicial proceedings.
              </div>
            </footer>
          </main>
        </>
      )}

      {/* Model Accuracy Specifications Modal */}
      <ModelAccuracyModal
        isOpen={isAccuracyModalOpen}
        onClose={() => setIsAccuracyModalOpen(false)}
      />
    </div>
  );
}
