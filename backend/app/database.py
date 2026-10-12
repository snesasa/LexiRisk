import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        filename TEXT,
        file_type TEXT,
        text TEXT NOT NULL,
        overall_risk_score REAL DEFAULT 0,
        risk_level TEXT DEFAULT 'Low',
        summary TEXT,
        stats_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clauses (
        id TEXT PRIMARY KEY,
        contract_id TEXT NOT NULL,
        clause_index INTEGER NOT NULL,
        section_title TEXT,
        text TEXT NOT NULL,
        category TEXT NOT NULL,
        confidence REAL DEFAULT 0.0,
        risk_score REAL DEFAULT 0.0,
        risk_level TEXT DEFAULT 'Low',
        risk_factors TEXT,
        explanation TEXT,
        redline_suggestion TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scenarios (
        id TEXT PRIMARY KEY,
        contract_id TEXT NOT NULL,
        title TEXT NOT NULL,
        trigger_event TEXT NOT NULL,
        probability TEXT NOT NULL,
        impact TEXT NOT NULL,
        dispute_type TEXT NOT NULL,
        description TEXT NOT NULL,
        triggered_clauses TEXT,
        mitigations TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_findings (
        id TEXT PRIMARY KEY,
        contract_id TEXT NOT NULL,
        finding_type TEXT NOT NULL,
        title TEXT NOT NULL,
        severity TEXT NOT NULL,
        description TEXT NOT NULL,
        recommendation TEXT,
        FOREIGN KEY (contract_id) REFERENCES contracts (id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

def save_contract_analysis(contract_data: Dict[str, Any], clauses: List[Dict[str, Any]], scenarios: List[Dict[str, Any]], findings: List[Dict[str, Any]]) -> str:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO contracts (id, title, filename, file_type, text, overall_risk_score, risk_level, summary, stats_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        contract_data['id'],
        contract_data['title'],
        contract_data.get('filename'),
        contract_data.get('file_type', 'text'),
        contract_data['text'],
        contract_data.get('overall_risk_score', 0),
        contract_data.get('risk_level', 'Low'),
        contract_data.get('summary', ''),
        json.dumps(contract_data.get('stats', {})),
        contract_data.get('created_at', datetime.utcnow().isoformat())
    ))

    # Clear existing clauses/scenarios for this contract if re-analyzing
    cursor.execute("DELETE FROM clauses WHERE contract_id = ?", (contract_data['id'],))
    cursor.execute("DELETE FROM scenarios WHERE contract_id = ?", (contract_data['id'],))
    cursor.execute("DELETE FROM audit_findings WHERE contract_id = ?", (contract_data['id'],))

    for c in clauses:
        cursor.execute("""
            INSERT INTO clauses (id, contract_id, clause_index, section_title, text, category, confidence, risk_score, risk_level, risk_factors, explanation, redline_suggestion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            c['id'],
            contract_data['id'],
            c['clause_index'],
            c.get('section_title', ''),
            c['text'],
            c['category'],
            c.get('confidence', 0.0),
            c.get('risk_score', 0.0),
            c.get('risk_level', 'Low'),
            json.dumps(c.get('risk_factors', [])),
            c.get('explanation', ''),
            c.get('redline_suggestion', '')
        ))

    for s in scenarios:
        cursor.execute("""
            INSERT INTO scenarios (id, contract_id, title, trigger_event, probability, impact, dispute_type, description, triggered_clauses, mitigations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            s['id'],
            contract_data['id'],
            s['title'],
            s['trigger_event'],
            s['probability'],
            s['impact'],
            s['dispute_type'],
            s['description'],
            json.dumps(s.get('triggered_clauses', [])),
            json.dumps(s.get('mitigations', []))
        ))

    for f in findings:
        unique_finding_id = f"{contract_data['id']}-{f['id']}"
        cursor.execute("""
            INSERT OR REPLACE INTO audit_findings (id, contract_id, finding_type, title, severity, description, recommendation)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            unique_finding_id,
            contract_data['id'],
            f['finding_type'],
            f['title'],
            f['severity'],
            f['description'],
            f.get('recommendation', '')
        ))

    conn.commit()
    conn.close()
    return contract_data['id']

def get_contract_by_id(contract_id: str) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    contract = dict(row)
    if contract.get('stats_json'):
        contract['stats'] = json.loads(contract['stats_json'])
    else:
        contract['stats'] = {}

    cursor.execute("SELECT * FROM clauses WHERE contract_id = ? ORDER BY clause_index ASC", (contract_id,))
    clauses = []
    for r in cursor.fetchall():
        item = dict(r)
        if item.get('risk_factors'):
            item['risk_factors'] = json.loads(item['risk_factors'])
        clauses.append(item)
    contract['clauses'] = clauses

    cursor.execute("SELECT * FROM scenarios WHERE contract_id = ?", (contract_id,))
    scenarios = []
    for r in cursor.fetchall():
        item = dict(r)
        if item.get('triggered_clauses'):
            item['triggered_clauses'] = json.loads(item['triggered_clauses'])
        if item.get('mitigations'):
            item['mitigations'] = json.loads(item['mitigations'])
        scenarios.append(item)
    contract['scenarios'] = scenarios

    cursor.execute("SELECT * FROM audit_findings WHERE contract_id = ?", (contract_id,))
    findings = [dict(r) for r in cursor.fetchall()]
    contract['findings'] = findings

    conn.close()
    return contract

def list_all_contracts() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, filename, file_type, overall_risk_score, risk_level, summary, created_at FROM contracts ORDER BY created_at DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def delete_contract_by_id(contract_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id,))
    cursor.execute("DELETE FROM clauses WHERE contract_id = ?", (contract_id,))
    cursor.execute("DELETE FROM scenarios WHERE contract_id = ?", (contract_id,))
    cursor.execute("DELETE FROM audit_findings WHERE contract_id = ?", (contract_id,))
    conn.commit()
    conn.close()
    return True
