import re
import uuid
from typing import List, Dict, Any
from .semantic_retriever import get_semantic_retriever

class ScenarioSimulator:
    """
    Simulates plausible future dispute scenarios and litigation risks based on contract wording.
    Provides automated scenario synthesis and interactive 'What-If' hypothetical testing.
    """

    PREDEFINED_ARCHETYPES = [
        {
            "id_prefix": "scen-uncapped-damages",
            "required_categories": ["Uncapped Liability"],
            "fallback_missing": "Missing Cap on Liability",
            "title": "Catastrophic Consequential Damages Claim Following Operational Outage",
            "dispute_type": "Unlimited Financial Damages Litigation",
            "probability": "High",
            "impact": "Critical",
            "trigger_event": "A temporary service disruption, security incident, or delayed milestone causes indirect commercial losses to the counterparty.",
            "description": (
                "Because liability is uncapped or consequential damages are not expressly waived, the counterparty files an unhedged "
                "claim demanding full recovery of third-party lost profits, reputational harm, and ancillary expenses. "
                "The lack of a monetary ceiling prevents insurance subrogation limits and exposes total company balance sheet capital."
            ),
            "escalation_timeline": [
                {"period": "Day 1-14", "event": "Notice of Material Default and assertion of consequential losses"},
                {"period": "Day 15-45", "event": "Formal damages assessment letter demanding damages far exceeding contract value"},
                {"period": "Day 60+", "event": "Litigation filing seeking freezing of accounts or full indemnity"}
            ],
            "mitigations": [
                "Insert an absolute mutual limitation of liability capped at 12 months fees paid.",
                "Explicitly disclaim lost profits, indirect, punitive, and consequential damages.",
                "Require formal cure period and limitation on time to bring claims (e.g., 1 year)."
            ]
        },
        {
            "id_prefix": "scen-mna-blocker",
            "required_categories": ["Change Of Control", "Anti-Assignment"],
            "title": "M&A Poison Pill: Hostile Contract Cancellation During Acquisition",
            "dispute_type": "Corporate Transaction Blockade",
            "probability": "Medium",
            "impact": "Critical",
            "trigger_event": "Your organization negotiates an equity investment, majority acquisition, or strategic corporate reorganization.",
            "description": (
                "The counterparty leverages the Change of Control or Anti-Assignment restriction to declare the merger an incurable breach. "
                "They threaten to immediately terminate core operational rights unless granted substantial fee renegotiations, or they attempt "
                "to block the due diligence approval process entirely."
            ),
            "escalation_timeline": [
                {"period": "Day 1-10", "event": "Due diligence audit flags change of control consent vulnerability"},
                {"period": "Day 15-30", "event": "Counterparty refuses consent or demands significant ransom fee payment"},
                {"period": "Day 45+", "event": "Transaction closing delayed or restructured with indemnity escrow"}
            ],
            "mitigations": [
                "Carve out corporate reorganizations, mergers, and sales of substantially all assets from consent requirements.",
                "Limit Change of Control termination rights strictly to acquisitions by direct named competitors.",
                "Ensure consent cannot be 'unreasonably withheld, conditioned, or delayed'."
            ]
        },
        {
            "id_prefix": "scen-convenience-cancellation",
            "required_categories": ["Termination For Convenience"],
            "title": "Sudden Convenience Termination Causing Stranded Capital & Severance",
            "dispute_type": "Unrecoverable Sunk Cost Dispute",
            "probability": "High",
            "impact": "High",
            "trigger_event": "Client undergoes executive restructuring or internal budget cutbacks and cancels the contract without cause.",
            "description": (
                "After your team completes major upfront staffing, custom tooling, and resource allocation, the counterparty issues "
                "an abrupt termination for convenience. Without an explicit wind-down fee or milestone payout clause, your organization is "
                "left bearing the entirety of non-cancelable third-party commitments and lost anticipated margin."
            ),
            "escalation_timeline": [
                {"period": "Day 1", "event": "Delivery of immediate termination letter without explanation"},
                {"period": "Day 15", "event": "Disputed final accounting regarding work-in-progress deliverables"},
                {"period": "Day 30+", "event": "Stranded employee reallocation and write-off of development costs"}
            ],
            "mitigations": [
                "Require minimum sixty (60) to ninety (90) days advance written notice for convenience termination.",
                "Mandate an early termination fee reflecting remaining committed contract value or incurred non-cancelable expenses.",
                "Condition termination on full payment for all work-in-progress up to the effective termination date."
            ]
        },
        {
            "id_prefix": "scen-ip-seizure",
            "required_categories": ["Ip Ownership Assignment"],
            "title": "Proprietary Core Asset Seizure & Pre-Existing IP Entanglement",
            "dispute_type": "Intellectual Property Ownership Contest",
            "probability": "Medium",
            "impact": "Critical",
            "trigger_event": "Following completion of deliverables, a disagreement occurs regarding whether underlying codebase and modules belong to client.",
            "description": (
                "Broad assignment language without clear background IP carve-outs leads the counterparty to assert full exclusive ownership "
                "over all scripts, architecture, and reusable toolkits created during engagement. They threaten copyright infringement "
                "if you deploy similar technology for other commercial clients."
            ),
            "escalation_timeline": [
                {"period": "Month 1", "event": "Client demands complete source repositories and assignment deed"},
                {"period": "Month 2", "event": "Cease & desist letter asserting ownership over core platform modules"},
                {"period": "Month 4+", "event": "Federal copyright/trade-secret litigation clouding corporate fundraising"}
            ],
            "mitigations": [
                "Clearly distinguish between Customer Bespoke Deliverables and Vendor Pre-Existing IP / Toolkits.",
                "Grant Customer a non-exclusive license to background IP rather than assigning outright title.",
                "Ensure assignment only vests upon full receipt of final agreed compensation."
            ]
        },
        {
            "id_prefix": "scen-evergreen-trap",
            "required_categories": ["Renewal Term", "Notice Period To Terminate Renewal"],
            "title": "Involuntary Evergreen Lock-in & Enforced Price Escalation",
            "dispute_type": "Unintended Term Extension & Payment Enforcement",
            "probability": "High",
            "impact": "Medium",
            "trigger_event": "Internal contract tracking misses the tight notice deadline to opt out of the successive contract term.",
            "description": (
                "Due to ambiguous or punitive notice windows (e.g. 90 days prior to year end), your organization fails to transmit written "
                "non-renewal notice in time. The counterparty automatically renews the contract for a multi-year term at increased prices, "
                "threatening immediate collections and breach proceedings if invoices are withheld."
            ),
            "escalation_timeline": [
                {"period": "30 Days Prior", "event": "Cancellation window quietly lapses without vendor reminder"},
                {"period": "Term End", "event": "Invoice issued for full year renewal with compounded rate increase"},
                {"period": "Post-Term", "event": "Collection demand with threat of statutory interest"}
            ],
            "mitigations": [
                "Require counterparty to provide written advance reminder 30 days prior to any renewal notice deadline.",
                "Require mutual written consent to renew rather than passive automatic extension.",
                "Cap any renewal price escalation to Consumer Price Index (CPI) with an upper ceiling of 3%."
            ]
        },
        {
            "id_prefix": "scen-non-compete-restraint",
            "required_categories": ["Non-Compete", "Exclusivity"],
            "title": "Anti-Competitive Market Preclusion & Commercial Injunction",
            "dispute_type": "Restrictive Covenant Enforcement Action",
            "probability": "Medium",
            "impact": "High",
            "trigger_event": "Your organization seeks to pitch products to a new customer operating in an adjacent or overlapping industry sector.",
            "description": (
                "The counterparty issues an immediate emergency preliminary injunction claim under the Non-Compete and Exclusivity provisions, "
                "asserting that your new client relationship violates territorial and product restrictions. The legal action freezes prospective "
                "revenue pipelines during crucial growth phases."
            ),
            "escalation_timeline": [
                {"period": "Week 1", "event": "Emergency demand letter demanding termination of prospective deal"},
                {"period": "Week 3", "event": "Motion for Temporary Restraining Order (TRO) filed in district court"},
                {"period": "Month 2+", "event": "Protracted restrictive covenant evidentiary hearing"}
            ],
            "mitigations": [
                "Limit non-compete scope strictly to directly competing bespoke projects for named competitors.",
                "Narrow geographic and market duration to maximum six (6) months post-contract.",
                "Explicitly carve out general industry consulting, generic software development, and off-the-shelf software."
            ]
        }
    ]

    def generate_scenarios(self, clauses: List[Dict[str, Any]], findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Synthesizes plausible dispute scenarios tailored to the contract's specific clauses.
        """
        detected_categories = {c.get("category") for c in clauses}
        generated = []

        for archetype in self.PREDEFINED_ARCHETYPES:
            req_cats = archetype["required_categories"]
            # Match if any required category is present
            matched_clauses = [c for c in clauses if c.get("category") in req_cats]
            
            # Check if high-risk clause matched or critical missing finding matched
            is_matched = bool(matched_clauses)
            if not is_matched and archetype.get("fallback_missing"):
                is_matched = any(f["title"] == archetype["fallback_missing"] for f in findings)

            if is_matched:
                scenario_id = f"{archetype['id_prefix']}-{uuid.uuid4().hex[:6]}"
                
                # Extract specific excerpts
                triggered_excerpts = []
                for c in matched_clauses[:3]:
                    triggered_excerpts.append({
                        "clause_index": c.get("clause_index"),
                        "category": c.get("category"),
                        "section_title": c.get("section_title"),
                        "excerpt": c.get("text")[:220] + "..." if len(c.get("text", "")) > 220 else c.get("text")
                    })

                generated.append({
                    "id": scenario_id,
                    "title": archetype["title"],
                    "trigger_event": archetype["trigger_event"],
                    "probability": archetype["probability"],
                    "impact": archetype["impact"],
                    "dispute_type": archetype["dispute_type"],
                    "description": archetype["description"],
                    "triggered_clauses": triggered_excerpts,
                    "escalation_timeline": archetype["escalation_timeline"],
                    "mitigations": archetype["mitigations"]
                })

        # Ensure at least 2 scenarios are generated even for benign contracts
        if len(generated) < 2 and clauses:
            # Add general breach scenario
            top_clause = sorted(clauses, key=lambda x: x.get("risk_score", 0), reverse=True)[0]
            generated.append({
                "id": f"scen-general-breach-{uuid.uuid4().hex[:6]}",
                "title": f"Disputed Performance & Material Default Under Section {top_clause.get('clause_index')}",
                "trigger_event": "A milestone disagreement or delayed deliverable leads to formal allegations of material contractual breach.",
                "probability": "Medium",
                "impact": "Medium",
                "dispute_type": "Breach of Performance Covenant",
                "description": (
                    f"Under Section '{top_clause.get('section_title', 'General Terms')}', differing expectations regarding acceptance "
                    "criteria and performance standards cause the counterparty to withhold payments and issue notice of default."
                ),
                "triggered_clauses": [{
                    "clause_index": top_clause.get("clause_index"),
                    "category": top_clause.get("category"),
                    "section_title": top_clause.get("section_title"),
                    "excerpt": top_clause.get("text")[:200]
                }],
                "escalation_timeline": [
                    {"period": "Day 1-15", "event": "Informal dispute notification and payment freeze"},
                    {"period": "Day 30", "event": "Notice of material breach demanding immediate remediation"},
                    {"period": "Day 60+", "event": "Arbitration or litigation filing"}
                ],
                "mitigations": [
                    "Define objective, unambiguous acceptance testing criteria with a deemed-acceptance period.",
                    "Include mandatory good-faith executive escalation meetings prior to formal legal action."
                ]
            })

        return generated

    def simulate_custom_hypothetical(self, hypothetical: str, clauses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Interactive 'What-If' scenario evaluator.
        Analyzes a custom hypothetical query against all contract clauses to pinpoint legal triggers and fallout.
        """
        retriever = get_semantic_retriever()
        similar = retriever.retrieve_similar_clauses(hypothetical, top_k=3)

        # Match relevant clauses in contract using semantic similarity or keyword overlap
        matched_contract_clauses = []
        hypo_lower = hypothetical.lower()

        for c in clauses:
            c_text = c.get("text", "").lower()
            overlap_score = 0
            for word in hypo_lower.split():
                if len(word) > 3 and word in c_text:
                    overlap_score += 1

            if overlap_score >= 2 or any(sim["category"] == c.get("category") for sim in similar):
                matched_contract_clauses.append({
                    "clause_index": c.get("clause_index"),
                    "category": c.get("category"),
                    "section_title": c.get("section_title"),
                    "risk_score": c.get("risk_score"),
                    "text": c.get("text")[:240] + "..." if len(c.get("text", "")) > 240 else c.get("text"),
                    "relevance_score": min(95, 40 + overlap_score * 15)
                })

        # Sort by relevance
        matched_contract_clauses.sort(key=lambda x: x["relevance_score"], reverse=True)
        top_matches = matched_contract_clauses[:3]

        # Determine projected outcome
        if any(m["risk_score"] >= 70 for m in top_matches):
            projected_risk = "Critical Risk"
            outcome_summary = "High likelihood of immediate breach assertion, injunctive action, or significant financial exposure without remedy cap."
        elif top_matches:
            projected_risk = "Moderate Exposure"
            outcome_summary = "Presents operational friction or contractual dispute; enforceability depends on written notice timing and cure compliance."
        else:
            projected_risk = "Low Contractual Impact"
            outcome_summary = "This hypothetical scenario does not directly trigger any heavily restricted clauses identified in the agreement."

        return {
            "hypothetical_query": hypothetical,
            "projected_risk": projected_risk,
            "outcome_summary": outcome_summary,
            "triggered_clauses": top_matches,
            "recommended_action": (
                "Review the triggered provisions with legal counsel to confirm whether formal cure notices or waiver agreements are required."
            )
        }

# Global singleton
_simulator_instance = None

def get_scenario_simulator() -> ScenarioSimulator:
    global _simulator_instance
    if _simulator_instance is None:
        _simulator_instance = ScenarioSimulator()
    return _simulator_instance
