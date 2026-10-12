import uuid
import json
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import DB_PATH
from .database import (
    init_db,
    save_contract_analysis,
    get_contract_by_id,
    list_all_contracts,
    delete_contract_by_id
)
from .services.document_parser import DocumentParser
from .services.clause_classifier import get_clause_classifier
from .services.semantic_retriever import get_semantic_retriever
from .services.risk_engine import get_risk_engine
from .services.scenario_simulator import get_scenario_simulator
from .services.export_service import ExportService
from .services.sample_contracts import SAMPLE_CONTRACTS
from .services.cuad_taxonomy import CUAD_CATEGORIES

app = FastAPI(
    title="AI-Powered Contract Clause Risk Analyzer",
    description="Local NLP legal intelligence system with CUAD 41-category classification and Future Scenario Detection",
    version="1.0.0"
)

# CORS middleware for React / Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    # Pre-warm classifier and retriever
    get_clause_classifier()
    get_semantic_retriever()
    get_risk_engine()
    get_scenario_simulator()

# --- Schemas ---
class AnalyzeTextRequest(BaseModel):
    title: str
    text: str
    filename: Optional[str] = "custom_contract.txt"

class CompareRequest(BaseModel):
    clause_a: str
    clause_b: Optional[str] = None
    category: Optional[str] = None

class SimulateRequest(BaseModel):
    contract_id: str
    hypothetical_query: str

# --- Pipeline Runner ---
def run_full_contract_analysis(contract_id: str, title: str, text: str, filename: str, file_type: str = "text") -> Dict[str, Any]:
    parser = DocumentParser()
    classifier = get_clause_classifier()
    risk_engine = get_risk_engine()
    simulator = get_scenario_simulator()

    # 1. Segment contract into clauses
    segmented = parser.segment_contract(text)
    analyzed_clauses = []
    detected_categories = []

    for item in segmented:
        c_text = item["text"]
        sec_title = item.get("section_title", "")
        
        # 2. Classify clause into 41 CUAD categories
        clf_res = classifier.classify_clause(c_text, sec_title)
        cat = clf_res["category"]
        conf = clf_res["confidence"]
        detected_categories.append(cat)

        # 3. Risk audit & redline generation
        risk_res = risk_engine.evaluate_clause(c_text, cat, sec_title)

        analyzed_clauses.append({
            "id": f"{contract_id}-c{item['clause_index']}",
            "clause_index": item["clause_index"],
            "section_title": sec_title,
            "text": c_text,
            "category": cat,
            "confidence": conf,
            "candidates": clf_res.get("candidates", []),
            "risk_score": risk_res["risk_score"],
            "risk_level": risk_res["risk_level"],
            "risk_factors": risk_res["risk_factors"],
            "explanation": risk_res["explanation"],
            "possible_consequences": risk_res["possible_consequences"],
            "redline_suggestion": risk_res["redline_suggestion"]
        })

    # 4. Audit missing protections
    missing_findings = risk_engine.audit_missing_protections(detected_categories)

    # 5. Composite overall risk score
    overall_score, overall_level = risk_engine.calculate_overall_risk(analyzed_clauses, missing_findings)

    # 6. Future Scenario Detection
    scenarios = simulator.generate_scenarios(analyzed_clauses, missing_findings)

    # Stats
    stats = {
        "total_clauses": len(analyzed_clauses),
        "critical_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Critical"),
        "high_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "High"),
        "medium_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Medium"),
        "low_count": sum(1 for c in analyzed_clauses if c["risk_level"] == "Low"),
        "missing_protections_count": len(missing_findings),
        "scenarios_count": len(scenarios)
    }

    summary = (
        f"Contract analysis complete. Identified {stats['total_clauses']} discrete clauses across {len(set(detected_categories))} unique legal categories. "
        f"Detected {stats['critical_count']} Critical and {stats['high_count']} High risk provisions, along with "
        f"{stats['missing_protections_count']} missing essential commercial protections. Overall posture is rated as {overall_level} Risk ({overall_score}/100)."
    )

    contract_data = {
        "id": contract_id,
        "title": title,
        "filename": filename,
        "file_type": file_type,
        "text": text,
        "overall_risk_score": overall_score,
        "risk_level": overall_level,
        "summary": summary,
        "stats": stats
    }

    # Save to database
    save_contract_analysis(contract_data, analyzed_clauses, scenarios, missing_findings)

    return get_contract_by_id(contract_id)

# --- Endpoints ---
@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "AI Contract Risk Analyzer", "version": "1.0.0"}

@app.get("/api/cuad/categories")
def get_cuad_categories():
    return CUAD_CATEGORIES

@app.get("/api/samples")
def get_sample_contracts():
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "filename": s["filename"],
            "description": s["description"],
            "preview": s["text"][:300] + "..."
        }
        for s in SAMPLE_CONTRACTS
    ]

@app.post("/api/samples/{sample_id}/load")
def load_sample_contract(sample_id: str):
    sample = next((s for s in SAMPLE_CONTRACTS if s["id"] == sample_id), None)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample contract not found")

    new_id = f"sample-{uuid.uuid4().hex[:8]}"
    result = run_full_contract_analysis(
        contract_id=new_id,
        title=sample["title"],
        text=sample["text"],
        filename=sample["filename"],
        file_type="sample"
    )
    return result

@app.post("/api/upload")
async def upload_contract(file: UploadFile = File(...), title: Optional[str] = Form(None)):
    contents = await file.read()
    raw_filename = file.filename or "uploaded_contract.txt"
    text = DocumentParser.parse_file(raw_filename, contents)
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Uploaded file contains no readable text.")

    contract_title = title if title and title.strip() else raw_filename.rsplit('.', 1)[0].replace('_', ' ').title()
    contract_id = f"cntr-{uuid.uuid4().hex[:8]}"

    result = run_full_contract_analysis(
        contract_id=contract_id,
        title=contract_title,
        text=text,
        filename=raw_filename,
        file_type=raw_filename.split('.')[-1]
    )
    return result

@app.post("/api/analyze-text")
def analyze_text(req: AnalyzeTextRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Contract text cannot be empty.")

    contract_id = f"cntr-{uuid.uuid4().hex[:8]}"
    result = run_full_contract_analysis(
        contract_id=contract_id,
        title=req.title,
        text=req.text,
        filename=req.filename or "direct_input.txt",
        file_type="text"
    )
    return result

@app.get("/api/contracts")
def get_all_contracts():
    return list_all_contracts()

@app.get("/api/contracts/{contract_id}")
def get_contract(contract_id: str):
    data = get_contract_by_id(contract_id)
    if not data:
        raise HTTPException(status_code=404, detail="Contract not found")
    return data

@app.delete("/api/contracts/{contract_id}")
def delete_contract(contract_id: str):
    success = delete_contract_by_id(contract_id)
    return {"success": success}

@app.post("/api/compare")
def compare_clauses_endpoint(req: CompareRequest):
    retriever = get_semantic_retriever()
    if req.clause_b:
        # Compare two custom clauses
        return retriever.compare_clauses(req.clause_a, req.clause_b)
    elif req.category:
        # Compare against CUAD market standard
        return retriever.compare_against_market_standard(req.clause_a, req.category)
    else:
        # Retrieve closest matching standard benchmark
        top_matches = retriever.retrieve_similar_clauses(req.clause_a, top_k=1)
        if top_matches:
            best_cat = top_matches[0]["category"]
            return retriever.compare_against_market_standard(req.clause_a, best_cat)
        raise HTTPException(status_code=400, detail="Provide clause_b or category for comparison.")

@app.post("/api/simulate")
def simulate_scenario_endpoint(req: SimulateRequest):
    contract = get_contract_by_id(req.contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    simulator = get_scenario_simulator()
    return simulator.simulate_custom_hypothetical(req.hypothetical_query, contract.get("clauses", []))

@app.get("/api/contracts/{contract_id}/export/{export_format}")
def export_contract_report(contract_id: str, export_format: str):
    contract = get_contract_by_id(contract_id)
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")

    if export_format.lower() == "markdown" or export_format.lower() == "md":
        md = ExportService.generate_markdown(contract)
        return Response(content=md, media_type="text/markdown", headers={
            "Content-Disposition": f"attachment; filename=\"{contract['title'].replace(' ', '_')}_risk_report.md\""
        })
    elif export_format.lower() == "html":
        html = ExportService.generate_html(contract)
        return Response(content=html, media_type="text/html", headers={
            "Content-Disposition": f"inline; filename=\"{contract['title'].replace(' ', '_')}_risk_report.html\""
        })
    elif export_format.lower() == "json":
        return contract
    else:
        raise HTTPException(status_code=400, detail="Supported export formats: markdown, html, json")
