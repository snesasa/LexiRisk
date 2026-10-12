# ⚖️ LexiRisk AI: Contract Clause Risk Analyzer with Future Scenario Detection

An intelligent, privacy-preserving legal contract intelligence platform designed to identify high-risk, ambiguous, incomplete, and conflicting clauses in commercial agreements. 

Trained and calibrated on the **Contract Understanding Atticus Dataset (CUAD)** across **41 legal categories**, the system combines NLP Transformer models, rule-based risk heuristics, semantic vector retrieval, and automated future dispute simulation to accelerate contract review.

---

## 🌟 Key Features

1. **41-Category CUAD Transformer Classification**:
   - Classifies clauses into official CUAD categories (e.g., *Uncapped Liability, Non-Compete, Exclusivity, Termination for Convenience, IP Ownership Assignment, Change of Control, Liquidated Damages, Most Favored Nation*).
   - Provides confidence scores and candidate category rankings.

2. **Multi-Factor Risk Scoring Engine (0-100)**:
   - Evaluates base legal risks, unilateral obligations, onerous penalties, and vague drafting (*"sole discretion"*, *"reasonable efforts"*, *"material breach"* without cure timelines).
   - Classifies findings into **Critical**, **High**, **Medium**, and **Low** risk profiles.

3. **Future Dispute Scenario Simulation**:
   - Synthesizes realistic future dispute scenarios based on exact contract wording.
   - Highlights trigger conditions, dispute likelihood, operational consequences, projected escalation timelines, and clause citations.
   - **Interactive "What-If" Simulator**: Enter custom hypothetical queries (e.g., *"What if our cloud platform experiences a 4-hour outage?"* or *"What if we get acquired?"*) and receive immediate exposure projections.

4. **Missing Core Protections Audit**:
   - Flags absent baseline protections such as **Cap on Liability**, **Renewal Notice Window**, **Governing Law**, and **Post-Termination Data Return**.
   - Provides 1-click ready-to-insert boilerplate clauses.

5. **Side-by-Side Clause Comparator**:
   - Benchmarks any contract clause against official **CUAD market standard precedent clauses**.
   - Calculates semantic similarity percentage, lexical divergence, and legal alignment diagnosis.

6. **Actionable Redlines & Human-in-the-Loop Review**:
   - Provides balanced, protective redline revisions for human counsel review.
   - One-click copy for quick drafting.

7. **Multi-Format Report Export**:
   - Instant export to **Printable HTML Report**, **Executive Markdown Summary (.md)**, and **Raw JSON Data**.

8. **100% Local Inference & Privacy**:
   - Runs locally without sending sensitive contracts or proprietary intellectual property to external AI APIs.

---

## 🏛️ System Architecture

```mermaid
flowchart TD
    UI[React Enterprise Dashboard / Vite (Port 5173)] -->|REST API| API[FastAPI Backend (Port 8000)]
    ST[Streamlit App (Optional)] --> API
    API --> PARSER[Document Parser: TXT / PDF / DOCX]
    PARSER --> CLF[Clause Classifier: 41 CUAD Categories]
    PARSER --> RET[Semantic Retriever: Market Benchmark Index]
    PARSER --> RISK[Risk Engine: Heuristic & Ambiguity Rules]
    CLF & RET & RISK --> SCENARIO[Future Scenario & Dispute Simulator]
    SCENARIO --> DB[(SQLite Database)]
    DB --> EXPORT[Export Engine: Markdown, HTML, JSON]
```

---

## 🚀 Quick Start Guide

### 1. Requirements
- Python 3.10+ (PyTorch 2.1+)
- Node.js v18+ & npm

### 2. Starting the FastAPI Backend
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
- API Docs: `http://127.0.0.1:8000/docs`
- Health Check: `http://127.0.0.1:8000/api/health`

### 3. Starting the React Enterprise Dashboard
```bash
cd frontend
npm run dev
```
- Web Application: `http://127.0.0.1:5173/`

### 4. (Optional) Starting the Companion Streamlit App
```bash
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
d:/NLP Project/
├── backend/
│   ├── app/
│   │   ├── config.py                  # Server configuration and directory paths
│   │   ├── database.py                # SQLite persistence for contracts, clauses, scenarios
│   │   ├── main.py                    # FastAPI application & REST endpoints
│   │   └── services/
│   │       ├── cuad_taxonomy.py       # 41 CUAD categories, benchmarks, and risk profiles
│   │       ├── document_parser.py     # TXT, DOCX, and PDF parsing & clause segmentation
│   │       ├── clause_classifier.py   # CUAD calibrated multi-class clause classifier
│   │       ├── semantic_retriever.py  # Market precedent indexing & clause comparator
│   │       ├── risk_engine.py         # Multi-factor risk scoring & missing protections audit
│   │       ├── scenario_simulator.py  # Future dispute simulation & interactive What-If engine
│   │       ├── sample_contracts.py    # Preloaded sample contracts (SaaS, NDA, Distributor)
│   │       └── export_service.py      # Markdown, HTML, and JSON report generator
│   └── data_cache/                    # Cached model parameters and embeddings
├── frontend/                          # Modern React + Vite Enterprise UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx             # Top bar, contract switcher, theme toggle
│   │   │   ├── RiskGauge.jsx          # Circular animated SVG risk score gauge
│   │   │   ├── DashboardOverview.jsx  # KPI metrics, category breakdown, top warnings
│   │   │   ├── ClauseInspector.jsx    # Verbatim excerpts, risk filters, redlines
│   │   │   ├── FutureScenarioExplorer.jsx # Scenarios & interactive What-If tester
│   │   │   ├── SideBySideComparator.jsx   # Clause vs precedent benchmark tool
│   │   │   ├── MissingProtectionsAudit.jsx # Boilerplate omissions audit
│   │   │   └── UploadModal.jsx        # Drag-and-drop file upload & sample contract loader
│   │   ├── App.jsx                    # Root view and navigation
│   │   └── index.css                  # Custom legal-tech design system (Vanilla CSS)
│   ├── package.json
│   └── vite.config.js
├── data/
│   └── CUADv1.json                    # Contract Understanding Atticus Dataset
├── streamlit_app.py                   # Companion Streamlit application
└── README.md
```

---

## ⚖️ Legal Practice Notice
LexiRisk AI is an automated decision-support tool created to assist human attorneys, legal teams, and contract reviewers. It does not constitute formal legal counsel, establish an attorney-client relationship, or guarantee legal enforceability in court.
