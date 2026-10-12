import re
from typing import Dict, Any, List, Tuple
from .cuad_taxonomy import CUAD_CATEGORIES, HIGH_RISK_CATEGORIES, STANDARD_REQUIRED_PROTECTIONS

class RiskEngine:
    """
    Comprehensive legal risk audit engine.
    Combines rule-based pattern matching, ambiguous language detection,
    missing protection auditing, and multi-factor risk scoring.
    """

    # Ambiguity patterns
    AMBIGUOUS_PATTERNS = [
        (r'\b(?:best\s+efforts|best\s+endeavours)\b', "Vague Standard: 'Best efforts' imposes an onerous, undefined burden under many legal jurisdictions.", 15),
        (r'\b(?:sole\s+discretion)\b', "Unilateral Discretion: Grants one party unchallengeable decision-making authority without reasonableness checks.", 20),
        (r'\b(?:material\s+breach)\b(?!.*\bdefined\b)', "Undefined Threshold: 'Material breach' is referenced without an objective definition or cure timetable.", 10),
        (r'\b(?:reasonable\s+efforts)\b', "Ambiguous Obligation: 'Reasonable efforts' lacks measurable objective milestones.", 8),
        (r'\b(?:from\s+time\s+to\s+time\s+at\s+its\s+option)\b', "Unpredictable Modification: Permits unilateral adjustments without advance counterparty notice.", 18),
        (r'\b(?:including\s+without\s+limitation)\b', "Open-Ended Scope: Broadens liability or operational exposure indefinitely.", 5)
    ]

    # Specific clause risk rules
    CLAUSE_RULES = {
        "Uncapped Liability": [
            (r'\b(?:without\s+limitation|no\s+(?:cap|limit)\s+on\s+liability|unlimited\s+liability)\b',
             "Explicit Uncapped Liability: The contract explicitly waives liability caps.", 30),
            (r'\b(?:indirect|consequential|punitive|special)\s+damages\b(?!.*\b(?:neither\s+party|shall\s+not\s+be\s+liable)\b)',
             "Consequential Damages Exposure: Special or consequential damages may not be disclaimed.", 25)
        ],
        "Termination For Convenience": [
            (r'\b(?:immediate(?:ly)?\s+upon\s+notice|without\s+(?:prior\s+)?notice)\b',
             "Abrupt Termination: Permits immediate termination without a transition or wind-down window.", 30),
            (r'\b(?:sole\s+option\s+of\s+(?:company|client|licensor|buyer))\b',
             "One-Sided Termination: Convenience termination is strictly unilateral rather than mutual.", 25)
        ],
        "Non-Compete": [
            (r'\b(?:worldwide|anywhere\s+in\s+the\s+world|no\s+geographic(?:al)?\s+limitation)\b',
             "Excessive Geographic Scope: Global non-compete may be ruled an illegal restraint of trade or cripple future growth.", 25),
            (r'\b(?:3|three|4|four|5|five)\s+years\b',
             "Protracted Duration: Multi-year restrictive covenant exceeds standard commercial reasonableness.", 20)
        ],
        "Ip Ownership Assignment": [
            (r'\b(?:all\s+inventions|all\s+works|all\s+developments)\b.*\b(?:sole\s+and\s+exclusive\s+property)\b',
             "Overbroad IP Seizure: Transfers all developments without carving out pre-existing background IP or tools.", 30),
            (r'\b(?:waives\s+all\s+moral\s+rights|irrevocably\s+assigns\s+in\s+perpetuity)\b',
             "Perpetual Assignment: Irrevocably forfeits rights without payment contingency.", 15)
        ],
        "Renewal Term": [
            (r'\b(?:automatically\s+renew(?:s|ed)?)\b(?!.*\b(?:written\s+notice)\b)',
             "Evergreen Trap: Contract auto-renews without clear cancellation notice requirement.", 25)
        ],
        "Liquidated Damages": [
            (r'\b(?:penalty|forfeiture)\b',
             "Punitive Damage Risk: Penal liquidated damages may be legally unenforceable or financially ruinous.", 20),
            (r'\b(?:daily\s+penalty|per\s+day\s+of\s+delay)\b(?!.*\b(?:capped|maximum)\b)',
             "Uncapped Daily Penalties: Liquidated damages compound daily without an aggregate ceiling.", 25)
        ],
        "Change Of Control": [
            (r'\b(?:terminate\s+immediately\s+upon\s+(?:any\s+)?change\s+of\s+control)\b',
             "M&A Poison Pill: Allows counterparty to cancel contract upon financing or merger event.", 25)
        ],
        "Governing Law": [
            (r'\b(?:foreign\s+jurisdiction|outside\s+the\s+united\s+states)\b',
             "Cross-Border Dispute Friction: Litigating outside domestic courts substantially increases legal expenses.", 15)
        ]
    }

    # Mitigation signals that lower risk
    MITIGATION_SIGNALS = [
        (r'\b(?:mutual(?:ly)?|both\s+parties)\b', 12),
        (r'\b(?:thirty\s+\(30\)\s+days|60\s+days|ninety\s+\(90\)\s+days)\s+(?:prior\s+)?written\s+notice\b', 15),
        (r'\b(?:capped\s+at|shall\s+not\s+exceed\s+the\s+total\s+fees)\b', 20),
        (r'\b(?:except\s+in\s+the\s+event\s+of\s+(?:gross\s+negligence|willful\s+misconduct))\b', 10),
        (r'\b(?:thirty\s+\(30\)\s+day\s+cure\s+period)\b', 15)
    ]

    def evaluate_clause(self, clause_text: str, category: str, section_title: str = "") -> Dict[str, Any]:
        """
        Calculates risk score, triggers, explanation, and redline suggestion for a clause.
        """
        category_meta = CUAD_CATEGORIES.get(category, {
            "title": category,
            "base_risk": 20,
            "description": "General contract provision.",
            "benchmark": "",
            "dispute_types": ["General Commercial Dispute"]
        })

        base_risk = category_meta.get("base_risk", 20)
        risk_score = float(base_risk)
        risk_factors = []
        consequences = []

        lower_text = clause_text.lower()

        # 1. Ambiguity audit
        for pattern, expl, penalty in self.AMBIGUOUS_PATTERNS:
            if re.search(pattern, lower_text, re.IGNORECASE):
                risk_score += penalty
                risk_factors.append(expl)

        # 2. Specific clause risk rules
        rules = self.CLAUSE_RULES.get(category, [])
        for pattern, expl, penalty in rules:
            if re.search(pattern, lower_text, re.IGNORECASE):
                risk_score += penalty
                risk_factors.append(expl)

        # 3. Mitigation signals (discount risk)
        for pattern, bonus in self.MITIGATION_SIGNALS:
            if re.search(pattern, lower_text, re.IGNORECASE):
                risk_score = max(5.0, risk_score - bonus)

        # Clamp risk score between 0 and 100
        risk_score = min(100.0, max(5.0, round(risk_score, 1)))

        # Determine Risk Level
        if risk_score >= 75:
            risk_level = "Critical"
        elif risk_score >= 50:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Generate Explanation
        explanation = self._build_explanation(category, risk_factors, risk_level, category_meta)

        # Generate Possible Consequences
        consequences = self._generate_consequences(category, risk_factors, risk_level, category_meta)

        # Generate Redline Suggestion
        redline = self._generate_redline_suggestion(clause_text, category, category_meta)

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "explanation": explanation,
            "possible_consequences": consequences,
            "redline_suggestion": redline
        }

    def _build_explanation(self, category: str, risk_factors: List[str], risk_level: str, meta: Dict[str, Any]) -> str:
        """Constructs concise, lawyer-grade explanation of findings."""
        if risk_factors:
            factors_summary = " ".join(risk_factors[:2])
            return f"This {category} clause presents {risk_level.lower()} risk. {factors_summary}"
        else:
            if risk_level in ["High", "Critical"]:
                return f"This provision involves {category}, a high-scrutiny commercial area that typically carries substantial obligations or indemnification duties."
            else:
                return f"Standard {category} wording with balanced commercial commitments."

    def _generate_consequences(self, category: str, risk_factors: List[str], risk_level: str, meta: Dict[str, Any]) -> List[str]:
        """Identifies concrete commercial fallout if this clause is invoked."""
        consequences = []
        if category == "Uncapped Liability":
            consequences.append("Potential catastrophic damages claim exceeding total contract remuneration.")
            consequences.append("Inability to cap insurance exposure or pass audit scrutiny.")
        elif category == "Termination For Convenience":
            consequences.append("Sudden loss of revenue without recovery for upfront investment costs.")
            consequences.append("Operational chaos due to abrupt workflow disruption without cure time.")
        elif category == "Non-Compete":
            consequences.append("Legal injunction blocking key product expansion or new customer acquisition.")
            consequences.append("Potential legal defense expenses in restrictive covenant litigation.")
        elif category == "Ip Ownership Assignment":
            consequences.append("Inadvertent transfer of proprietary software algorithms, tooling, or background IP.")
            consequences.append("Diminished company valuation during investor due diligence.")
        elif category == "Change Of Control":
            consequences.append("Acquisition blocker or hostile contract termination triggered during merger/acquisition.")
        elif category == "Liquidated Damages":
            consequences.append("Automatic cash deductions from payments prior to formal dispute resolution.")
        elif category == "Renewal Term":
            consequences.append("Involuntary continuation of contract for an additional year at unfavorable terms.")
        else:
            disputes = meta.get("dispute_types", ["Commercial Breach"])
            consequences.append(f"Heightened risk of {disputes[0].lower()} under adverse market conditions.")
        return consequences

    def _generate_redline_suggestion(self, clause_text: str, category: str, meta: Dict[str, Any]) -> str:
        """Suggests balanced, protective alternative language."""
        benchmark = meta.get("benchmark", "")
        if category == "Uncapped Liability":
            return (
                "PROPOSED REVISION:\n"
                "\"Except for gross negligence, willful misconduct, or breach of Section [Confidentiality], "
                "neither party's total aggregate liability arising out of or related to this Agreement shall exceed "
                "the total fees paid or payable by Customer hereunder in the twelve (12) months preceding the claim.\""
            )
        elif category == "Termination For Convenience":
            return (
                "PROPOSED REVISION:\n"
                "\"Either party may terminate this Agreement without cause upon sixty (60) days prior written notice "
                "to the other party, provided that Customer shall pay for all authorized deliverables satisfactorily "
                "completed up to the effective termination date.\""
            )
        elif category == "Non-Compete":
            return (
                "PROPOSED REVISION:\n"
                "\"During the Term and for a period of six (6) months thereafter, Provider shall not directly solicit "
                "Customer's exclusive clients introduced solely under this Statement of Work within the primary operating territory.\""
            )
        elif category == "Ip Ownership Assignment":
            return (
                "PROPOSED REVISION:\n"
                "\"Customer shall own all rights in bespoke deliverables created specifically for Customer, excluding "
                "Provider's Pre-Existing IP, core libraries, generic algorithms, and toolkits, for which Customer is granted "
                "a perpetual, non-exclusive license.\""
            )
        elif category == "Renewal Term" or category == "Notice Period To Terminate Renewal":
            return (
                "PROPOSED REVISION:\n"
                "\"This Agreement shall renew for successive one (1) year terms only upon mutual written agreement, or unless "
                "either party provides written notice of non-renewal at least thirty (30) days prior to the end of the then-current term.\""
            )
        elif benchmark:
            return f"MARKET STANDARD BENCHMARK:\n\"{benchmark}\""
        else:
            return "RECOMMENDATION: Insert mutual notice requirements, a 30-day cure period, and an express liability limitation."

    def audit_missing_protections(self, detected_categories: List[str]) -> List[Dict[str, Any]]:
        """
        Examines contract-wide classified categories to identify absent core legal protections.
        """
        findings = []
        detected_set = set(detected_categories)

        for req in STANDARD_REQUIRED_PROTECTIONS:
            cat = req["category"]
            if cat not in detected_set:
                findings.append({
                    "id": f"missing-{cat.lower().replace(' ', '-')}",
                    "finding_type": "Missing Protection",
                    "title": req["title"],
                    "severity": req["severity"],
                    "description": req["description"],
                    "recommendation": req["recommendation"]
                })

        return findings

    def calculate_overall_risk(self, clauses: List[Dict[str, Any]], missing_findings: List[Dict[str, Any]]) -> Tuple[float, str]:
        """
        Computes composite overall contract risk score (0-100) and risk level classification.
        """
        if not clauses:
            return 0.0, "Low"

        scores = [c.get("risk_score", 0) for c in clauses]
        critical_count = sum(1 for s in scores if s >= 75)
        high_count = sum(1 for s in scores if 50 <= s < 75)
        
        # Weighted score: top 3 highest risk clauses + average baseline + missing protection penalties
        top_scores = sorted(scores, reverse=True)[:3]
        top_avg = sum(top_scores) / len(top_scores) if top_scores else 0
        overall_avg = sum(scores) / len(scores)

        missing_penalty = sum(10 for f in missing_findings if f["severity"] == "Critical") + \
                          sum(5 for f in missing_findings if f["severity"] == "High")

        composite = (top_avg * 0.6) + (overall_avg * 0.25) + missing_penalty
        final_score = min(100.0, max(5.0, round(composite, 1)))

        if final_score >= 70 or critical_count >= 2:
            level = "Critical"
        elif final_score >= 50 or high_count >= 2 or critical_count >= 1:
            level = "High"
        elif final_score >= 30:
            level = "Medium"
        else:
            level = "Low"

        return final_score, level

# Global singleton
_risk_engine_instance = None

def get_risk_engine() -> RiskEngine:
    global _risk_engine_instance
    if _risk_engine_instance is None:
        _risk_engine_instance = RiskEngine()
    return _risk_engine_instance
