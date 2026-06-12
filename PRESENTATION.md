# TrustSphere AI — Presentation Deck

## Slide Deck Outline (15 Slides)

Designed for a 20-minute presentation to hiring managers, governance teams, or portfolio review.

---

### Slide 1: Title Slide
**TrustSphere AI**
*Enterprise AI Governance · Risk · Compliance · Third-Party Risk Management*

Subtitle: "From spreadsheets to structured governance — one platform for vendor risk, AI compliance, and regulatory reporting."

---

### Slide 2: The Problem
**Organisations Are Adopting AI Faster Than They Can Govern It**

- Every week: new AI vendor, new chatbot deployment, new regulation
- Compliance teams rely on: **spreadsheets, email chains, fragmented tools**
- The result: **inconsistent assessments, no audit trail, regulatory exposure**

Quote: *"60%+ of data breaches come through third-party vendors."* — IBM

---

### Slide 3: The Solution
**TrustSphere AI — One Platform for the Full Governance Lifecycle**

| Capability | What It Solves |
|---|---|
| **Vendor Due Diligence** | Consistent 4-domain scoring, no more spreadsheets |
| **AI Risk Assessment** | EU AI Act classification, risk factors, controls |
| **DPIA** | GDPR-compliant privacy impact assessments |
| **Policy Review** | Gap analysis against 7 regulatory frameworks |
| **Risk Register** | Track, score, and mitigate risks |
| **Human-in-the-Loop** | Role-based approvals, SLA, 2-person rule |
| **Audit Trail** | Tamper-evident, verifiable, regulator-ready |
| **PDF Reports** | Board-ready, executive-summary-first |

---

### Slide 4: Who Uses It

| Role | What They Care About |
|---|---|
| **NHS IG Officer** | DSP Toolkit compliance, patient data safety |
| **Banking TPRM Lead** | DORA, FCA SYSC 8, vendor concentration risk |
| **AI Governance Manager** | EU AI Act conformity, risk classification |
| **Data Protection Officer** | DPIAs, GDPR Art. 35/36, third-country transfers |
| **Compliance Officer** | Policy gaps, remediation tracking, evidence |
| **Procurement Manager** | Consistent vendor scoring, audit trail |

---

### Slide 5: Architecture Overview

[Show the architecture diagram from README]

Nine integrated modules sharing:
- Common audit layer (HMAC-SHA256 hash chain)
- Human-in-the-loop approval framework
- Professional PDF reporting engine
- Module registry for extensibility

---

### Slide 6: Live Demo — OpenAI (GPT-4o API)

**Scenario:** Complete vendor risk assessment for OpenAI's GPT-4o API

[Show the demo output]

| Metric | Value |
|---|---|
| Vendor Risk Score | 1.20/5.00 (Low) |
| DPIA Result | HIGH — DPO Required |
| AI Risk Rating | UNACCEPTABLE (5/5) |
| Approval Status | APPROVED (with conditions) |
| Risk Factors Detected | 4 (sensitive data, profiling, vulnerable groups, automated decisions) |
| Risk Register | 6 items (1 critical) |
| PDF Reports Generated | 4 |

---

### Slide 7: Vendor Due Diligence Deep Dive

**4-Domain Weighted Scoring**

| Domain | Weight | Key Factors |
|---|---|---|
| Security | 35% | SOC2, ISO27001, encryption, MFA, breach history |
| Financial | 25% | Audited financials, cyber insurance, profitability |
| Compliance | 25% | GDPR, CCPA, HIPAA, regulatory investigations |
| Operational | 15% | BCP/DR, sub-processors, SLA, criticality |

**3 Tiers:**
- 1.0–2.0 → **Low** (auto-approve)
- 2.1–3.5 → **Medium** (risk analyst review, 48h SLA)
- 3.6–5.0 → **High** (compliance officer, 24h SLA, 2-person override)

---

### Slide 8: AI Risk Assessment (EU AI Act)

**4 Risk Categories**

| Category | Score | Meaning | Requirements |
|---|---|---|---|
| Unacceptable | 5 | Contravenes EU AI Act prohibitions | Do not deploy |
| High | 4 | High-risk under Annex III | Conformity assessment, DPIA, human oversight |
| Limited | 2 | Transparency obligations | Explainability, user notice |
| Minimal | 1 | Low governance risk | Standard data governance |

**Risk factors checked:**
Healthcare diagnosis, credit scoring, recruitment, law enforcement, critical infrastructure, sensitive data, vulnerable groups, profiling, automated decisions

---

### Slide 9: DPIA Assessment (GDPR Art. 35/36)

**Privacy Impact Assessment Pipeline**

Input: Processing purpose, data categories, subjects
→ Privacy impacts identified and scored
→ GDPR articles mapped (Art. 5–49)
→ DPO consultation determination
→ Prior authority assessment
→ Recommendations generated

**Example Output:**
```
Overall Risk:     HIGH
DPO Required:     YES
Prior Authority:  YES
GDPR Articles:    12
Recommendations:  9
```

---

### Slide 10: Policy Review — Gap Analysis

**Multi-Framework Compliance Checking**

| Framework | Requirements Checked |
|---|---|
| ISO 27001 | Access control, encryption, incident response, BC/DR |
| NHS DSP Toolkit | Confidentiality, data quality, supplier assurance |
| DORA | ICT risk management, incident reporting, resilience testing |
| FCA SYSC 8 | Outsourcing, third-party risk |
| SOX | Internal controls, financial reporting |
| NIST AI RMF | Govern, Map, Measure, Manage |
| UK DPA 2018 | Lawful processing, special category data |

**Scoring:**
- Coverage % = requirements met / total requirements
- Risk score = weighted severity of gaps (0–10)
- Severity: Critical, High, Medium, Low

---

### Slide 11: Human-in-the-Loop Approval

```
Low Risk ──────► Auto-Approve + Audit
Medium ────────► Risk Analyst (48h SLA) → Approve/Reject/Escalate
High ──────────► Compliance Officer (24h SLA) → 2-person override rule

Decisions: Approve · Reject · Re-assess · Override · Request Evidence
```

**Controls:**
- Role-based assignment per risk tier
- SLA enforcement with automatic escalation
- Two-person rule for score overrides
- Full audit trail of every decision
- Escalation: Risk Analyst → Compliance Officer → AI Governance Lead

---

### Slide 12: Audit Trail (Tamper-Evident)

**HMAC-SHA256 Hash Chain**

```
Event 0 (genesis)          Event 1                   Event 2
hash = HMAC("0x0" + d0)    hash = HMAC(h0 + d1)      hash = HMAC(h1 + d2)
prev = 0x0...              prev = h0                  prev = h1
```

- Each event stores previous event's hash
- Verify chain recomputes from genesis → tip
- Any tampering breaks the chain immediately
- JSONL export for regulator submission

---

### Slide 13: Professional PDF Reports

**5 Report Types**

| Report | Contents | Audience |
|---|---|---|
| Vendor DD Report | Risk score, domain breakdown, governance, audit | Procurement, Risk |
| DPIA Report | Processing overview, impacts, GDPR articles, recs | DPO, ICO |
| AI Risk Report | EU AI Act class, risk factors, controls, compliance | AI Governance |
| Policy Review Report | Coverage %, gaps by severity, remediation | Compliance |
| Combined Governance | Executive summary of all assessments | Board, C-suite |

All reports include:
- Cover page with branding and metadata
- Executive summary with KPI cards
- Data tables with risk color coding
- Audit trail summary
- Disclaimer and confidentiality notice

---

### Slide 14: Skills Map

| Skill | Evidence |
|---|---|
| **AI Governance** | EU AI Act classification, risk factors, human oversight tiers |
| **Third-Party Risk** | 4-domain scoring, flags, rationale, vendor lifecycle |
| **Data Protection** | GDPR Art. 35/36 DPIAs, DPO consultation, prior authority |
| **Compliance** | 7-framework gap analysis, severity scoring, remediation |
| **Risk Management** | Inherent/residual scoring, heatmap, regulatory mapping |
| **Python Engineering** | Pydantic, dataclasses, FastAPI, ReportLab, 54 tests |
| **System Design** | 9-module archipelago, registry pattern, shared infra |

---

### Slide 15: What's Next / Roadmap

**Current (Complete):**
- ✅ Core scoring engine with 4 domains
- ✅ AI Risk, DPIA, Policy Review modules
- ✅ Risk Register with inherent/residual scoring
- ✅ Human-in-the-loop approval workflow
- ✅ HMAC audit chain with tamper detection
- ✅ Executive dashboard with approval UI
- ✅ Professional PDF reports (5 types)
- ✅ 54 tests, all passing
- ✅ End-to-end OpenAI demo scenario
- ✅ Branding, documentation, presentation

**Planned:**
- 🔜 Multi-tenant database persistence (SQLite → PostgreSQL)
- 🔜 SSO / OAuth2 authentication
- 🔜 Role-based access control
- 🔜 CI/CD pipeline with GitHub Actions
- 🔜 Docker containerization
- 🔜 Terraform deployment

---

## Presentation Tips

| Time | Slide | Focus |
|---|---|---|
| 0–2 min | 1–2 | Hook: "AI governance is broken. Here's the fix." |
| 2–5 min | 3–5 | Solution + architecture: "9 modules, shared infrastructure" |
| 5–10 min | 6–9 | Live demo: OpenAI scenario with real outputs |
| 10–15 min | 10–13 | Deep dive: policy review, human-in-the-loop, audit, reports |
| 15–18 min | 14 | Skills demonstration: "What this proves about my engineering" |
| 18–20 min | 15 | Roadmap + Q&A |

### Key Talking Points

- "I built this because regulated organisations can't assess AI risk at scale with spreadsheets"
- "Every module is tested independently — 54 tests, all passing"
- "The audit chain is the foundation — tamper-evident, verifiable, regulator-ready"
- "PDF reports are the output governance teams actually need — board-ready, not code"
- "This is a working governance platform, not a learning exercise"
