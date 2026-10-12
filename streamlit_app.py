import streamlit as st
import json
import uuid
from datetime import datetime
import pandas as pd

from backend.app.services.document_parser import DocumentParser
from backend.app.services.clause_classifier import get_clause_classifier
from backend.app.services.semantic_retriever import get_semantic_retriever
from backend.app.services.risk_engine import get_risk_engine
from backend.app.services.scenario_simulator import get_scenario_simulator
from backend.app.services.sample_contracts import SAMPLE_CONTRACTS
from backend.app.services.export_service import ExportService
from backend.app.database import init_db, save_contract_analysis, get_contract_by_id, list_all_contracts

st.set_page_config(
    page_title="LexiRisk AI - Contract Risk & Future Scenario Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .metric-card {
        background-color: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .badge-critical { background-color: #ef4444; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-high { background-color: #f97316; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-medium { background-color: #eab308; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
    .badge-low { background-color: #10b981; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

st.title("⚖️ LexiRisk AI: Contract Clause Risk Analyzer")
st.caption("CUAD v1.0 • 41 Categories • Local NLP Transformer & Future Dispute Scenario Simulation")

# Sidebar
st.sidebar.header("📁 Contract Source")
source_option = st.sidebar.radio("Choose Input Method", ["Preloaded Sample Contracts", "Upload Document (TXT/PDF/DOCX)", "Paste Contract Text"])

active_contract = None

def run_analysis(text: str, title: str, filename: str = "contract.txt"):
    with st.spinner("Analyzing contract clauses with CUAD NLP models and simulating dispute scenarios..."):
        parser = DocumentParser()
        classifier = get_clause_classifier()
        risk_engine = get_risk_engine()
        simulator = get_scenario_simulator()

        contract_id = f"st-{uuid.uuid4().hex[:8]}"
        segmented = parser.segment_contract(text)
        analyzed_clauses = []
        detected_categories = []

        for item in segmented:
            c_text = item["text"]
            sec_title = item.get("section_title", "")
            clf_res = classifier.classify_clause(c_text, sec_title)
            cat = clf_res["category"]
            detected_categories.append(cat)
            risk_res = risk_engine.evaluate_clause(c_text, cat, sec_title)

            analyzed_clauses.append({
                "id": f"{contract_id}-c{item['clause_index']}",
                "clause_index": item["clause_index"],
                "section_title": sec_title,
                "text": c_text,
                "category": cat,
                "confidence": clf_res["confidence"],
                "risk_score": risk_res["risk_score"],
                "risk_level": risk_res["risk_level"],
                "risk_factors": risk_res["risk_factors"],
                "explanation": risk_res["explanation"],
                "possible_consequences": risk_res["possible_consequences"],
                "redline_suggestion": risk_res["redline_suggestion"]
            })

        missing_findings = risk_engine.audit_missing_protections(detected_categories)
        overall_score, overall_level = risk_engine.calculate_overall_risk(analyzed_clauses, missing_findings)
        scenarios = simulator.generate_scenarios(analyzed_clauses, missing_findings)

        stats = {
            "total_clauses": len(analyzed_clauses),
            "critical_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Critical"),
            "high_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "High"),
            "medium_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Medium"),
            "low_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Low"),
            "missing_protections_count": len(missing_findings),
            "scenarios_count": len(scenarios)
        }

        contract_data = {
            "id": contract_id,
            "title": title,
            "filename": filename,
            "file_type": filename.split('.')[-1],
            "text": text,
            "overall_risk_score": overall_score,
            "risk_level": overall_level,
            "summary": f"Audit of {title} identified {len(analyzed_clauses)} clauses. Overall posture: {overall_level} Risk ({overall_score}/100).",
            "stats": stats
        }

        save_contract_analysis(contract_data, analyzed_clauses, scenarios, missing_findings)
        return get_contract_by_id(contract_id)

if source_option == "Preloaded Sample Contracts":
    sample_titles = [s["title"] for s in SAMPLE_CONTRACTS]
    selected_sample_title = st.sidebar.selectbox("Select Sample Contract", sample_titles)
    selected_sample = next(s for s in SAMPLE_CONTRACTS if s["title"] == selected_sample_title)
    
    st.sidebar.info(selected_sample["description"])
    if st.sidebar.button("Analyze Sample Contract", type="primary"):
        active_contract = run_analysis(selected_sample["text"], selected_sample["title"], selected_sample["filename"])
        st.session_state["current_contract"] = active_contract

elif source_option == "Upload Document (TXT/PDF/DOCX)":
    uploaded_file = st.sidebar.file_uploader("Upload File", type=["txt", "pdf", "docx"])
    custom_title = st.sidebar.text_input("Contract Title (Optional)")
    if uploaded_file and st.sidebar.button("Run Document Analysis", type="primary"):
        text = DocumentParser.parse_file(uploaded_file.name, uploaded_file.read())
        title = custom_title.strip() or uploaded_file.name.rsplit('.', 1)[0].replace('_', ' ').title()
        active_contract = run_analysis(text, title, uploaded_file.name)
        st.session_state["current_contract"] = active_contract

elif source_option == "Paste Contract Text":
    paste_title = st.sidebar.text_input("Contract Title", value="Custom Commercial Agreement")
    paste_text = st.sidebar.text_area("Paste Contract Text Here", height=200)
    if paste_text.strip() and st.sidebar.button("Analyze Pasted Text", type="primary"):
        active_contract = run_analysis(paste_text, paste_title)
        st.session_state["current_contract"] = active_contract

# Retrieve from session state if available
if "current_contract" in st.session_state and not active_contract:
    active_contract = st.session_state["current_contract"]

# Auto-run first sample if no contract loaded
if not active_contract:
    existing = list_all_contracts()
    if existing:
        active_contract = get_contract_by_id(existing[0]["id"])
    else:
        sample = SAMPLE_CONTRACTS[0]
        active_contract = run_analysis(sample["text"], sample["title"], sample["filename"])
        st.session_state["current_contract"] = active_contract

if active_contract:
    # Top Metrics Banner
    st.markdown("---")
    col_score, col_crit, col_high, col_scen, col_miss = st.columns(5)
    
    score = active_contract.get("overall_risk_score", 0)
    level = active_contract.get("risk_level", "Low")
    stats = active_contract.get("stats", {})

    col_score.metric("Overall Risk Score", f"{score}/100", f"{level} Risk", delta_color="inverse")
    col_crit.metric("Critical Clauses", stats.get("critical_count", 0))
    col_high.metric("High Severity", stats.get("high_count", 0))
    col_scen.metric("Dispute Scenarios", len(active_contract.get("scenarios", [])))
    col_miss.metric("Missing Protections", len(active_contract.get("findings", [])))

    st.subheader(active_contract.get("title"))
    st.write(active_contract.get("summary"))

    # Tabs
    tab_clauses, tab_scenarios, tab_compare, tab_missing, tab_export = st.tabs([
        f"📋 Clauses ({len(active_contract.get('clauses', []))})",
        f"🔮 Future Scenarios ({len(active_contract.get('scenarios', []))})",
        "⚖️ Side-by-Side Comparator",
        f"🛡️ Missing Protections ({len(active_contract.get('findings', []))})",
        "📥 Export Reports"
    ])

    with tab_clauses:
        col_f1, col_f2 = st.columns([1, 2])
        risk_filter = col_f1.selectbox("Filter by Risk Level", ["All", "Critical", "High", "Medium", "Low"])
        search_filter = col_f2.text_input("Search clause text or category")

        clauses = active_contract.get("clauses", [])
        for c in clauses:
            if risk_filter != "All" and c["risk_level"] != risk_filter:
                continue
            if search_filter and (search_filter.lower() not in c["text"].lower() and search_filter.lower() not in c["category"].lower()):
                continue

            with st.expander(f"Clause #{c['clause_index']}: {c['category']} — [{c['risk_level']} Risk ({c['risk_score']}/100)]"):
                st.markdown(f"**Section:** {c.get('section_title', 'General')}")
                st.code(c["text"], language="text")
                st.write(f"**Analysis:** {c['explanation']}")
                if c.get("risk_factors"):
                    st.write("**Identified Red Flags:**")
                    for rf in c["risk_factors"]:
                        st.markdown(f"- ⚠️ {rf}")
                if c.get("redline_suggestion"):
                    st.markdown("**Proposed Protective Revision (Human Review):**")
                    st.info(c["redline_suggestion"])

    with tab_scenarios:
        st.markdown("### Interactive What-If Scenario Simulator")
        user_hypo = st.text_input("Enter a hypothetical dispute event:", placeholder="e.g. What if the counterparty terminates early?")
        if user_hypo and st.button("Simulate"):
            sim = get_scenario_simulator()
            result = sim.simulate_custom_hypothetical(user_hypo, active_contract.get("clauses", []))
            st.success(f"**Projected Exposure:** {result['projected_risk']}")
            st.write(result["outcome_summary"])
            if result.get("triggered_clauses"):
                st.write("**Triggered Contract Clauses:**")
                for tc in result["triggered_clauses"]:
                    st.markdown(f"- **Clause {tc['clause_index']} ({tc['category']}):** {tc['text']}")

        st.markdown("---")
        st.markdown("### Identified Contract Dispute Scenarios")
        for s in active_contract.get("scenarios", []):
            st.error(f"**{s['title']}** (Likelihood: {s['probability']} | Impact: {s['impact']})")
            st.write(f"**Trigger:** {s['trigger_event']}")
            st.write(s['description'])
            if s.get("mitigations"):
                st.write("**Actionable Mitigations:**")
                for m in s["mitigations"]:
                    st.markdown(f"- {m}")
            st.markdown("---")

    with tab_compare:
        retriever = get_semantic_retriever()
        st.markdown("### Benchmark Against CUAD Market Standard Precedents")
        clauses = active_contract.get("clauses", [])
        if clauses:
            clause_opts = [f"Clause #{c['clause_index']}: {c['category']}" for c in clauses]
            sel_idx = st.selectbox("Select Clause from Contract", range(len(clause_opts)), format_func=lambda i: clause_opts[i])
            chosen_c = clauses[sel_idx]

            comp = retriever.compare_against_market_standard(chosen_c["text"], chosen_c["category"])
            sim_pct = comp.get("comparison", {}).get("similarity_percentage", 0) if comp.get("comparison") else 0
            
            st.metric("Semantic Similarity to Market Precedent", f"{sim_pct}%")
            if comp.get("comparison"):
                st.write(f"**Diagnosis:** {comp['comparison']['diagnosis']}")

            c1, c2 = st.columns(2)
            c1.markdown("**Your Contract Clause:**")
            c1.code(chosen_c["text"], language="text")

            c2.markdown(f"**CUAD Market Benchmark ({comp.get('benchmark_title', chosen_c['category'])}):**")
            c2.code(comp.get("benchmark_text", "No benchmark available"), language="text")

    with tab_missing:
        st.markdown("### Missing Standard Legal Protections")
        findings = active_contract.get("findings", [])
        if not findings:
            st.success("All core standard protections were detected in this agreement.")
        else:
            for f in findings:
                st.warning(f"**{f['severity']} Omission: {f['title']}**")
                st.write(f['description'])
                st.info(f"**Recommended Remedy:** {f['recommendation']}")

    with tab_export:
        st.markdown("### Export Full Legal Risk Report")
        md_report = ExportService.generate_markdown(active_contract)
        html_report = ExportService.generate_html(active_contract)

        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.download_button("Download Markdown (.md)", data=md_report, file_name=f"{active_contract['title']}_risk_report.md", mime="text/markdown")
        col_d2.download_button("Download Printable HTML (.html)", data=html_report, file_name=f"{active_contract['title']}_risk_report.html", mime="text/html")
        col_d3.download_button("Download Raw JSON (.json)", data=json.dumps(active_contract, indent=2), file_name=f"{active_contract['title']}_data.json", mime="application/json")

st.sidebar.markdown("---")
st.sidebar.caption("⚖️ LexiRisk AI is an automated contract intelligence tool. It does not provide formal legal counsel.")
