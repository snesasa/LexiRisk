"""
CUAD Taxonomy Definition:
Contains all 41 legal categories from the Contract Understanding Atticus Dataset (CUAD),
along with risk profiles, typical vulnerabilities, market standard clauses, and future dispute risks.
"""

from typing import Dict, Any, List

CUAD_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "Document Name": {
        "title": "Document Name",
        "description": "The formal title or name identifying the legal agreement.",
        "base_risk": 5,
        "keywords": ["agreement", "contract", "memorandum", "undertaking", "addendum", "amendment"],
        "benchmark": "THIS MASTER SERVICES AGREEMENT (the 'Agreement') is entered into...",
        "dispute_types": ["Contract Misclassification"],
        "critical": False
    },
    "Parties": {
        "title": "Parties",
        "description": "The exact legal entities entering into the contract, including corporate registration details.",
        "base_risk": 20,
        "keywords": ["by and between", "corporation", "limited liability company", "partners", "assigns", "successors"],
        "benchmark": "This Agreement is made by and between Company A, a Delaware corporation ('Client'), and Company B, a California corporation ('Vendor').",
        "dispute_types": ["Identity Dispute", "Lack of Authority / Ultra Vires"],
        "critical": False
    },
    "Agreement Date": {
        "title": "Agreement Date",
        "description": "The execution date on which the contract was signed or formally dated.",
        "base_risk": 10,
        "keywords": ["dated as of", "signed this", "execution date"],
        "benchmark": "Dated as of October 1, 2026.",
        "dispute_types": ["Pre-contractual Reliance", "Statute of Limitations"],
        "critical": False
    },
    "Effective Date": {
        "title": "Effective Date",
        "description": "The date when the rights, duties, and enforceability of the agreement become active.",
        "base_risk": 25,
        "keywords": ["effective date", "shall take effect on", "commencing on", "in force as of"],
        "benchmark": "This Agreement shall become effective upon the date of mutual execution ('Effective Date').",
        "dispute_types": ["Retroactive Liability Gap", "Premature Obligations"],
        "critical": False
    },
    "Expiration Date": {
        "title": "Expiration Date",
        "description": "The date or event upon which the contract's initial term naturally concludes.",
        "base_risk": 30,
        "keywords": ["shall expire on", "expiration date", "initial term shall end", "conclude on"],
        "benchmark": "This Agreement shall expire two (2) years from the Effective Date unless earlier terminated in accordance with Section 8.",
        "dispute_types": ["Post-Expiration Zombie Contract", "Lapse of Warranties"],
        "critical": False
    },
    "Renewal Term": {
        "title": "Renewal Term",
        "description": "Conditions governing automatic or optional extension of the agreement term.",
        "base_risk": 55,
        "keywords": ["automatically renew", "subsequent terms", "evergreen", "renewal period", "successive periods"],
        "benchmark": "This Agreement may be renewed for successive one (1) year periods upon mutual written consent of both parties.",
        "dispute_types": ["Unintended Evergreen Lock-in", "Unexpected Price Escalation"],
        "critical": False
    },
    "Notice Period To Terminate Renewal": {
        "title": "Notice Period To Terminate Renewal",
        "description": "Mandatory prior written notice required to prevent automatic contract extension.",
        "base_risk": 65,
        "keywords": ["written notice at least", "days prior to renewal", "prevent automatic renewal", "notice of non-renewal"],
        "benchmark": "Either party may prevent renewal by providing written notice of non-renewal at least thirty (30) days prior to the end of the current term.",
        "dispute_types": ["Missed Termination Window", "Forced Involuntary Renewal"],
        "critical": True
    },
    "Governing Law": {
        "title": "Governing Law",
        "description": "Jurisdiction and substantive laws regulating interpretation and dispute enforcement.",
        "base_risk": 45,
        "keywords": ["governed by and construed in accordance with", "laws of the state of", "jurisdiction", "venue"],
        "benchmark": "This Agreement shall be governed by, and construed under, the laws of the State of Delaware, without regard to its conflict of law principles.",
        "dispute_types": ["Foreign Jurisdiction Burden", "Unfavorable Precedent Exposure"],
        "critical": False
    },
    "Most Favored Nation": {
        "title": "Most Favored Nation",
        "description": "Covenant ensuring a party receives terms, pricing, or benefits as favorable as any third-party counterparty.",
        "base_risk": 75,
        "keywords": ["most favored nation", "mfn", "no less favorable than", "as favorable as granted to any other customer"],
        "benchmark": "Vendor agrees that pricing offered shall be no less favorable than pricing offered to similarly situated commercial customers for identical volumes.",
        "dispute_types": ["Margin Compression Claim", "Pricing Transparency Breach"],
        "critical": True
    },
    "Non-Compete": {
        "title": "Non-Compete",
        "description": "Restrictions barring a party or its affiliates from engaging in competitive business activities.",
        "base_risk": 85,
        "keywords": ["shall not engage in", "competitive business", "directly or indirectly compete", "covenant not to compete", "prohibited business"],
        "benchmark": "Neither party shall directly solicit or conduct competing operations in the territory during the term and for six (6) months thereafter, strictly limited to the core contracted product lines.",
        "dispute_types": ["Antitrust / Unreasonable Restraint of Trade", "Total Market Preclusion"],
        "critical": True
    },
    "Exclusivity": {
        "title": "Exclusivity",
        "description": "Prohibitions against contracting with competitors or granting exclusive rights within a territory or domain.",
        "base_risk": 80,
        "keywords": ["exclusive rights", "sole and exclusive", "shall not engage any third party", "sole distributor"],
        "benchmark": "Customer designates Provider as its non-exclusive supplier of the specified services for the designated territory.",
        "dispute_types": ["Supply Bottleneck Dispute", "Exclusivity Violation Breach Claim"],
        "critical": True
    },
    "No-Solicit Of Customers": {
        "title": "No-Solicit Of Customers",
        "description": "Restrictions preventing solicitation or enticement of customers or client relationships.",
        "base_risk": 60,
        "keywords": ["solicit or induce any customer", "divert business", "canvass clients", "interfere with contractual relationships"],
        "benchmark": "During the term, neither party shall specifically target or solicit existing customers of the other party introduced solely under this Agreement.",
        "dispute_types": ["Tortious Interference Allegation", "Customer Poaching Damages Claim"],
        "critical": False
    },
    "Competitive Restriction Exception": {
        "title": "Competitive Restriction Exception",
        "description": "Carve-outs and express exemptions from non-compete or exclusivity limitations.",
        "base_risk": 35,
        "keywords": ["notwithstanding anything to the contrary", "permitted to engage", "carve-out", "shall not be deemed a violation"],
        "benchmark": "Nothing herein shall prevent Provider from offering general software consulting services to entities that do not directly duplicate Customer's proprietary application.",
        "dispute_types": ["Ambiguous Scope of Permitted Activities"],
        "critical": False
    },
    "No-Solicit Of Employees": {
        "title": "No-Solicit Of Employees",
        "description": "Restrictions barring hiring, recruiting, or soliciting the counterparty's staff or contractors.",
        "base_risk": 50,
        "keywords": ["solicit, recruit, or hire", "personnel", "key employees", "induce any employee to leave"],
        "benchmark": "Neither party shall actively solicit for employment any key technical employee of the other party directly assigned to the project for a period of twelve (12) months.",
        "dispute_types": ["Talent Poaching Injunction", "Loss of Critical Personnel Claim"],
        "critical": False
    },
    "Non-Disparagement": {
        "title": "Non-Disparagement",
        "description": "Obligation prohibiting negative, derogatory, or defamatory public or private statements.",
        "base_risk": 40,
        "keywords": ["disparaging statements", "derogatory remarks", "harm the reputation", "shall not disparage"],
        "benchmark": "Both parties agree to refrain from making untruthful or defamatory public statements regarding the other party.",
        "dispute_types": ["Free Speech Restraint", "Public Review / Whistleblower Dispute"],
        "critical": False
    },
    "Termination For Convenience": {
        "title": "Termination For Convenience",
        "description": "The right to cancel the agreement at will without requiring proof of breach or fault.",
        "base_risk": 75,
        "keywords": ["terminate without cause", "at any time upon written notice", "for convenience", "without penalty"],
        "benchmark": "Either party may terminate this Agreement without cause upon providing sixty (60) days prior written notice, subject to payment for completed milestones.",
        "dispute_types": ["Sunk Capital Recovery Dispute", "Premature Contract Cancellation"],
        "critical": True
    },
    "Rofr/Rofo/Rofn": {
        "title": "ROFR / ROFO / ROFN",
        "description": "Right of First Refusal, First Offer, or First Negotiation on sales, assets, or licenses.",
        "base_risk": 65,
        "keywords": ["right of first refusal", "right of first offer", "rofr", "rofo", "first negotiation"],
        "benchmark": "In the event of an intended third-party asset sale, Licensor grants Licensee a ten (10) day right of first negotiation to purchase said rights.",
        "dispute_types": ["Transaction Delay & Deal Sabotage", "Preemptive Right Bypass Lawsuit"],
        "critical": False
    },
    "Change Of Control": {
        "title": "Change Of Control",
        "description": "Clauses triggered by mergers, acquisitions, sales of substantial assets, or management shifts.",
        "base_risk": 80,
        "keywords": ["change of control", "merger, consolidation", "sale of substantially all assets", "voting securities"],
        "benchmark": "In the event of a Change of Control to a direct competitor of Customer, Customer may terminate this Agreement upon thirty (30) days written notice.",
        "dispute_types": ["Blocked M&A Exit", "Poison Pill Trigger during Acquisition"],
        "critical": True
    },
    "Anti-Assignment": {
        "title": "Anti-Assignment",
        "description": "Restrictions requiring written consent before transferring contract rights or delegating obligations.",
        "base_risk": 60,
        "keywords": ["shall not assign or transfer", "without prior written consent", "any attempted assignment shall be null and void"],
        "benchmark": "Neither party may assign this Agreement without prior written consent, except to a corporate successor in connection with a merger or reorganization.",
        "dispute_types": ["Invalid Corporate Transfer", "Blocked Corporate Restructuring"],
        "critical": False
    },
    "Revenue/Profit Sharing": {
        "title": "Revenue/Profit Sharing",
        "description": "Provisions mandating distribution of royalties, commission percentages, or gross revenue splits.",
        "base_risk": 70,
        "keywords": ["percentage of gross revenue", "royalty calculation", "net profits", "revenue share", "commission"],
        "benchmark": "Party B shall remit 15% of Net Collected Revenue from designated products within thirty (30) days of quarter close.",
        "dispute_types": ["Audit Shortfall Dispute", "Divergence in Revenue Accounting Definitions"],
        "critical": False
    },
    "Price Restrictions": {
        "title": "Price Restrictions",
        "description": "Limits on price hikes, indexing formulas, price caps, or maximum annual inflation adjustments.",
        "base_risk": 55,
        "keywords": ["annual price increase shall not exceed", "cpi adjustment", "fixed pricing", "price ceiling"],
        "benchmark": "Provider may increase fees annually by no more than the Consumer Price Index (CPI) or 3%, whichever is lower, upon sixty (60) days written notice.",
        "dispute_types": ["Inflation Loss Lock-in", "Disputed Cost Pass-Through"],
        "critical": False
    },
    "Minimum Commitment": {
        "title": "Minimum Commitment",
        "description": "Obligations guaranteeing minimum purchase volume, usage quotas, or 'take-or-pay' spending.",
        "base_risk": 75,
        "keywords": ["minimum purchase commitment", "take or pay", "minimum annual spend", "shortfall payment"],
        "benchmark": "Buyer agrees to a non-binding quarterly forecast, with firm binding orders submitted thirty (30) days ahead.",
        "dispute_types": ["Unfulfilled Minimum Fee Penalties", "Take-or-Pay Shortfall Litigation"],
        "critical": True
    },
    "Volume Restriction": {
        "title": "Volume Restriction",
        "description": "Limits capping the quantity of products, seats, or bandwidth permitted under the agreement.",
        "base_risk": 50,
        "keywords": ["maximum volume", "seat limit", "bandwidth cap", "overage charges apply"],
        "benchmark": "Usage exceeding 100,000 monthly active users shall incur standard tiered overage rates set forth in Schedule A.",
        "dispute_types": ["Unexpected Overage Fee Claims", "Service Throttling / Outage Claims"],
        "critical": False
    },
    "Ip Ownership Assignment": {
        "title": "IP Ownership Assignment",
        "description": "Covenants assigning intellectual property rights, inventions, patents, and work products.",
        "base_risk": 90,
        "keywords": ["all right, title and interest", "work made for hire", "hereby irrevocably assigns", "proprietary rights", "inventions"],
        "benchmark": "Customer retains all rights to its pre-existing materials and confidential data. Provider retains all rights to its background software, core libraries, and generic tools.",
        "dispute_types": ["Loss of Background IP", "Customer Seizure of Proprietary Platform Code"],
        "critical": True
    },
    "Joint Ip Ownership": {
        "title": "Joint IP Ownership",
        "description": "Co-ownership frameworks for intellectual property created jointly by both contracting parties.",
        "base_risk": 85,
        "keywords": ["jointly owned", "tenants in common", "co-owners of intellectual property", "joint inventors"],
        "benchmark": "Neither party shall seek joint ownership of technology; all newly created IP shall be allocated exclusively to either Party A or Party B with a cross-license.",
        "dispute_types": ["Gridlock in Patent Filing / Licensing", "Independent Commercialization Cannibalization"],
        "critical": True
    },
    "License Grant": {
        "title": "License Grant",
        "description": "Terms defining the scope, duration, territory, and field of use for software or IP licenses.",
        "base_risk": 60,
        "keywords": ["hereby grants a license", "non-exclusive, non-transferable", "scope of license", "right to use"],
        "benchmark": "Licensor grants Licensee a non-exclusive, non-transferable, revocable license to access the hosted software during the subscription term.",
        "dispute_types": ["Exceeded Scope of License Lawsuit", "Copyright Infringement Allegation"],
        "critical": False
    },
    "Non-Transferable License": {
        "title": "Non-Transferable License",
        "description": "Prohibition against sublicensing, assigning, or sharing software licenses with third parties.",
        "base_risk": 50,
        "keywords": ["non-transferable", "may not sublicense", "strictly personal to licensee"],
        "benchmark": "The license is personal, non-transferable, and may not be sublicensed without prior written consent.",
        "dispute_types": ["Affiliate Sublicense Breach", "Unauthorized Outsourcing Breach"],
        "critical": False
    },
    "Affiliate License-Licensor": {
        "title": "Affiliate License-Licensor",
        "description": "Provisions enabling licensor affiliates to provide or exercise licensed rights.",
        "base_risk": 40,
        "keywords": ["licensor affiliates", "provided through affiliates", "parent and subsidiary companies"],
        "benchmark": "Licensor may perform obligations through its wholly-owned subsidiaries, remaining fully liable for their acts.",
        "dispute_types": ["Affiliate Performance Default"],
        "critical": False
    },
    "Affiliate License-Licensee": {
        "title": "Affiliate License-Licensee",
        "description": "Rights permitting licensee subsidiaries or parent companies to access and utilize the license.",
        "base_risk": 45,
        "keywords": ["licensee affiliates may use", "subsidiaries entitled to access", "enterprise-wide use"],
        "benchmark": "Licensee's majority-owned corporate affiliates may use the Software subject to compliance with all terms hereof.",
        "dispute_types": ["Unmetered Affiliate Expansion", "Audit Overreach"],
        "critical": False
    },
    "Unlimited/All-You-Can-Eat-License": {
        "title": "Unlimited / Enterprise License",
        "description": "Enterprise-wide grant permitting unbounded deployment, users, or compute capacity.",
        "base_risk": 55,
        "keywords": ["unlimited users", "enterprise-wide deployment", "no volume cap", "all-you-can-eat"],
        "benchmark": "Licensee is granted enterprise-wide deployment rights within the defined business unit during the active subscription period.",
        "dispute_types": ["Infrastructure Resource Exhaustion", "Contract Renewal Disagreements"],
        "critical": False
    },
    "Irrevocable Or Perpetual License": {
        "title": "Irrevocable / Perpetual License",
        "description": "License grant that cannot be rescinded and survives termination of commercial terms.",
        "base_risk": 75,
        "keywords": ["perpetual license", "irrevocable", "survives termination", "fully paid-up royalty-free"],
        "benchmark": "Upon full payment of delivery fees, Customer receives a perpetual, non-exclusive license to use deliverables solely for internal operations.",
        "dispute_types": ["Inability to Revoke upon Breach", "Loss of Recurring Revenue Leverage"],
        "critical": True
    },
    "Source Code Escrow": {
        "title": "Source Code Escrow",
        "description": "Deposit of software source code with an independent escrow agent released upon insolvency.",
        "base_risk": 65,
        "keywords": ["source code escrow", "escrow agent", "release condition", "bankruptcy or liquidation"],
        "benchmark": "Vendor agrees to deposit source code in escrow, to be released solely upon insolvency, bankruptcy, or permanent cessation of maintenance.",
        "dispute_types": ["Premature Release of Proprietary Source Code", "Escrow Maintenance Cost Dispute"],
        "critical": False
    },
    "Post-Termination Services": {
        "title": "Post-Termination Services",
        "description": "Transition assistance, data export, and decommissioning support after contract conclusion.",
        "base_risk": 60,
        "keywords": ["transition assistance", "post-termination support", "data return and export", "disentanglement services"],
        "benchmark": "Upon termination, Vendor shall provide up to ninety (90) days of reasonable transition services at standard time-and-materials rates.",
        "dispute_types": ["Hostage Data Extortion", "Post-Termination Run-Rate Fee Disputes"],
        "critical": False
    },
    "Audit Rights": {
        "title": "Audit Rights",
        "description": "The right to inspect premises, books, servers, and systems for contract and fee compliance.",
        "base_risk": 65,
        "keywords": ["right to audit", "inspect books and records", "upon reasonable notice", "underpayment penalty"],
        "benchmark": "Upon thirty (30) business days written notice, Licensor may conduct an annual audit during normal business hours without disrupting operations.",
        "dispute_types": ["Disruptive Forensic Audits", "Inflated Disputed Underpayment Invoices"],
        "critical": False
    },
    "Uncapped Liability": {
        "title": "Uncapped Liability",
        "description": "Absence of monetary ceiling or exclusion of consequential damages, exposing limitless financial exposure.",
        "base_risk": 100,
        "keywords": ["shall not be limited", "uncapped liability", "without limitation", "no ceiling on damages", "all damages whatsoever"],
        "benchmark": "Neither party shall face uncapped liability except for willful misconduct, gross negligence, or breach of confidentiality obligations.",
        "dispute_types": ["Catastrophic Company-Busting Lawsuit", "Uncapped Consequential Damages Claim"],
        "critical": True
    },
    "Cap On Liability": {
        "title": "Cap On Liability",
        "description": "Defines an explicit maximum financial ceiling (e.g. fees paid over past 12 months) for all claims.",
        "base_risk": 50,
        "keywords": ["aggregate liability shall not exceed", "maximum liability capped at", "fees paid in the prior twelve months", "limitation of liability"],
        "benchmark": "Each party's maximum aggregate liability shall not exceed the total fees paid under this Agreement in the twelve (12) months preceding the incident.",
        "dispute_types": ["Damages Cap Avoidance via Carve-Outs", "Inadequate Remedy for Catastrophic Breach"],
        "critical": True
    },
    "Liquidated Damages": {
        "title": "Liquidated Damages",
        "description": "Pre-agreed financial penalties for delayed delivery, SLA breaches, or specific defaults.",
        "base_risk": 75,
        "keywords": ["liquidated damages", "pre-agreed penalty", "per day of delay", "service level credit"],
        "benchmark": "Liquidated damages for delayed delivery shall equal 0.5% per week of delay, capped at 5% of total contract value, representing sole and exclusive remedy.",
        "dispute_types": ["Unenforceable Penalty Defense", "Immediate Cash Drain upon Minor Delay"],
        "critical": True
    },
    "Warranty Duration": {
        "title": "Warranty Duration",
        "description": "The time frame during which deliverables are warranted to operate in conformity with specs.",
        "base_risk": 45,
        "keywords": ["warranty period", "warranted for ninety days", "free from defects for a period of", "express warranty"],
        "benchmark": "Vendor warrants the software shall conform to documentation for ninety (90) days following acceptance.",
        "dispute_types": ["Latent Defect Claims after Warranty Expiry", "Disputed Warranty Voiding"],
        "critical": False
    },
    "Insurance": {
        "title": "Insurance",
        "description": "Covenants requiring maintenance of commercial general liability, errors & omissions, or cyber insurance policies.",
        "base_risk": 40,
        "keywords": ["commercial general liability", "errors and omissions", "cyber insurance", "additional insured", "certificate of insurance"],
        "benchmark": "Provider shall maintain $2,000,000 Commercial General Liability and $5,000,000 Errors & Omissions insurance with reputable carriers.",
        "dispute_types": ["Uninsured Loss Exposure", "Cancellation of Coverage Default"],
        "critical": False
    },
    "Covenant Not To Sue": {
        "title": "Covenant Not To Sue",
        "description": "A binding agreement refraining from asserting patent or IP infringement claims against the other party.",
        "base_risk": 70,
        "keywords": ["covenant not to sue", "shall not assert any claim", "waives right to bring action", "patent peace"],
        "benchmark": "Party A covenants not to initiate patent litigation against Party B for products deployed under this Agreement during the term.",
        "dispute_types": ["Surrendered Defensive Rights", "Scope of Covenant Ambiguity"],
        "critical": True
    },
    "Third Party Beneficiary": {
        "title": "Third Party Beneficiary",
        "description": "Determines whether entities not party to the contract possess direct rights of enforcement.",
        "base_risk": 55,
        "keywords": ["third party beneficiary", "no rights conferred upon third parties", "enforceable by any third party"],
        "benchmark": "Except as explicitly provided regarding indemnified affiliates, this Agreement does not confer any rights upon any third party.",
        "dispute_types": ["End-User Direct Lawsuit", "Subcontractor Direct Enforcement"],
        "critical": False
    }
}

# Categories considered high risk or red flags
HIGH_RISK_CATEGORIES = {
    "Uncapped Liability",
    "Non-Compete",
    "Exclusivity",
    "Ip Ownership Assignment",
    "Joint Ip Ownership",
    "Change Of Control",
    "Termination For Convenience",
    "Minimum Commitment",
    "Liquidated Damages",
    "Most Favored Nation",
    "Irrevocable Or Perpetual License",
    "Covenant Not To Sue"
}

# Core protections that should NOT be missing from standard commercial contracts
STANDARD_REQUIRED_PROTECTIONS = [
    {
        "category": "Cap On Liability",
        "title": "Missing Cap on Liability",
        "severity": "Critical",
        "description": "The agreement does not contain an express monetary cap on liability (e.g., 12-month trailing fees), leaving both parties vulnerable to unlimited consequential and direct damages.",
        "recommendation": "Insert a mutual limitation of liability clause: 'Neither party's aggregate liability under this Agreement shall exceed the total fees paid or payable in the 12 months prior to the event giving rise to liability.'"
    },
    {
        "category": "Notice Period To Terminate Renewal",
        "title": "Missing Renewal Cancellation Notice Window",
        "severity": "High",
        "description": "The agreement does not specify a clear 30-to-60 day written notice deadline to cancel renewal, risking unintentional evergreen lock-in.",
        "recommendation": "Specify: 'Either party may terminate the automatic renewal by providing written notice at least thirty (30) days prior to the expiration of the current term.'"
    },
    {
        "category": "Governing Law",
        "title": "Missing Governing Law & Jurisdiction",
        "severity": "Medium",
        "description": "No governing law or dispute venue is defined, which can result in costly jurisdictional battles if litigation arises.",
        "recommendation": "Add a standard governing law clause selecting a predictable commercial jurisdiction (e.g., Delaware or New York) and mandatory venue."
    },
    {
        "category": "Post-Termination Services",
        "title": "Missing Data Return & Post-Termination Transition",
        "severity": "Medium",
        "description": "No clear procedure exists for data destruction, transition assistance, or IP return upon agreement conclusion.",
        "recommendation": "Include a data return clause: 'Within thirty (30) days following termination, Vendor shall deliver or securely delete all Customer confidential data.'"
    }
]
