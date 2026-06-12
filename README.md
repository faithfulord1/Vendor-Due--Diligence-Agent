# TrustSphere AI

**Enterprise AI Governance · Risk · Compliance · Third-Party Risk Management**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-54%20passing-brightgreen)](tests/)
[![AI Governance](https://img.shields.io/badge/focus-AI%20Governance-purple)](#)
[![GRC](https://img.shields.io/badge/capability-GRC-teal)](#)
[![NHS](https://img.shields.io/badge/industry-NHS%20%7C%20Banking%20%7C%20Gov-orange)](#)

---

## The Story

> **"Organisations are adopting AI rapidly, but struggle to assess vendor risk, perform DPIAs, review policies, and comply with AI governance requirements."**

I built TrustSphere AI because governance and compliance teams are fighting a losing battle with spreadsheets, fragmented tools, and manual processes. Every week another vendor integrates AI, another department deploys a chatbot, another regulation takes effect. The tools to manage this complexity don't exist off the shelf — so I built one.

This platform helps governance and compliance teams **perform structured assessments** and **generate executive-ready reports** across:
- **Vendor Due Diligence** — risk scoring, flags, domain breakdowns
- **AI Risk Assessment** — EU AI Act classification, governance controls, human oversight
- **DPIA (Data Protection Impact Assessment)** — GDPR Art. 35/36, privacy impacts, DPO consultation
- **Policy Review** — gap analysis against ISO 27001, NHS DSP Toolkit, DORA, and more
- **Risk Register** — inherent/residual scoring, heatmap, regulatory mapping
- **Audit Trail** — HMAC-SHA256 tamper-evident hash chain
- **Human-in-the-Loop Approval** — role-based routing, SLA enforcement, two-person rule
- **Professional PDF Reports** — board-ready, executive-summary-first, with full audit trail

### Who would use it?

| Role | Why they care |
|---|---|
| **NHS Information Governance Officer** | Assess AI vendors against DSP Toolkit, manage patient data risk |
| **Banking TPRM Lead** | Vendor risk scoring aligned with DORA, FCA SYSC 8, PRA SS2/21 |
| **AI Governance Manager** | Classify AI systems under EU AI Act, generate conformity evidence |
| **Data Protection Officer (DPO)** | Automate DPIAs, map GDPR articles, manage third-country transfers |
| **Compliance Officer** | Review policies, identify gaps, track remediation |
| **Procurement Manager** | Vendor due diligence with consistent scoring and audit trail |

### Why does it matter?

- **AI regulation is here** — EU AI Act, NHS AI guidance, FCA AI rules
- **Third-party risk is exploding** — 60%+ of breaches come through vendors
- **Manual processes don't scale** — spreadsheets are not compliant
- **Regulators demand evidence** — audit trails, DPIAs, risk assessments

---

## Screenshots

| | |
|---|---|
| ![Executive Dashboard](screenshots/dashboard.svg) | ![Risk Assessment](screenshots/risk-assessment.svg) |
| **Executive Dashboard** — Live KPI cards, risk register, pending approvals with Approve/Reject/Escalate actions, governance status, audit trail, AI risk classification | **Vendor Risk Assessment** — 4-domain scoring breakdown, aggregate score, elevated flags, governance gate results, AI/DPIA risk summary |
| ![PDF Report Preview](screenshots/pdf-report-preview.svg) | ![Architecture Diagram](screenshots/architecture.svg) |
| **Professional PDF Reports** — Board-ready reports with score summary, domain breakdown, audit trail, and compliance metadata | **Platform Architecture** — 4-layer design: Ingestion → Assessment → Governance → Audit & Output |

---

## Platform Architecture

```
                     ┌──────────────────────────────────────┐
                     │   EXECUTIVE DASHBOARD                 │
                     │   PROFESSIONAL PDF REPORTS            │
                     │   (Board-ready, executive-summary)    │
                     └────────────────┬─────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
           ▼                          ▼                          ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│ Vendor Due          │  │ AI Risk Assessment  │  │ Policy Review       │
│ Diligence           │  │ (EU AI Act)        │  │ (Gap Analysis)      │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ • 4-domain scoring  │  │ • Risk factors     │  │ • Coverage %        │
│ • Elevated flags    │  │ • Governance ctrls │  │ • Severity scoring  │
│ • Rationale engine  │  │ • Human oversight  │  │ • NHS/Banking reqs  │
└──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
           │                        │                        │
           ▼                        ▼                        ▼
┌───────────────────────────────────────────────────────────────────────┐
│                        RISK REGISTER                                   │
│              (Inherent / residual scoring, heatmap)                    │
├───────────────────────────────────────────────────────────────────────┤
│                   HUMAN-IN-THE-LOOP APPROVAL                           │
│     (Role-based routing · SLA enforcement · 2-person rule)            │
├───────────────────────────────────────────────────────────────────────┤
│                   AUDIT LOGGER (HMAC-SHA256)                          │
│          Tamper-evident hash chain across ALL modules                  │
└───────────────────────────────────────────────────────────────────────┘
```

### Nine Integrated Modules

| # | Module | Status | Tests | What It Does |
|---|---|---|---|---|
| 1 | **Vendor Due Diligence** | Complete | 14 | Score vendors across security, financial, compliance, operational domains with risk tiers, flags, and rationale |
| 2 | **AI Risk Assessment** | Complete | 8 | Classify AI systems under EU AI Act (Unacceptable/High/Limited/Minimal) with risk factors, governance controls, and oversight recommendations |
| 3 | **DPIA Assessment** | Complete | 11 | GDPR Art. 35/36 compliant privacy impact assessments with DPO consultation, prior authority, and article mapping |
| 4 | **Policy Review** | Complete | 10 | Gap analysis against ISO 27001, NHS DSP Toolkit, DORA, FCA, SOX with coverage %, severity, and remediation |
| 5 | **Risk Register** | Complete | 11 | Inherent/residual risk scoring, heatmap, category grouping, by-vendor filtering, regulatory references |
| 6 | **Audit Logger** | Complete | 3 | HMAC-SHA256 tamper-evident hash chain with genesis-to-tip verification, event filtering, JSONL export |
| 7 | **Human-in-the-Loop** | Complete | 3 | Role-based assignment, SLA enforcement, escalation, approve/reject/override/request-evidence, 2-person rule |
| 8 | **Executive Dashboard** | Complete | — | Live KPI cards, risk table, heatmap, vendor/AI distribution, governance status, audit trail, approval action buttons |
| 9 | **Professional PDF Reports** | Complete | — | Board-ready Vendor DD, DPIA, AI Risk, Policy Review, and Integrated Governance reports with cover pages, tables, KPIs, audit trails |

---

## Demo Scenario: OpenAI (GPT-4o API)

```bash
python demo_openai.py
```

### Output Summary

```
Vendor:               OpenAI (GPT-4o API)
Risk Score:           1.20/5.00
Risk Tier:            Low
Elevated Flags:       1
Governance Gates:     PASSED

DPIA Result:          REQUIRED
DPIA Overall Risk:    HIGH
GDPR Articles:        12
DPIA Recommendations: 9

AI Risk Rating:       UNACCEPTABLE
AI Risk Score:        5/5
AI Risk Factors:      4
Controls Required:    0
Requires Conformity:  NO

Approval Status:      APPROVED
Review Role:          risk_analyst
Final Score:          2.50

Risk Register:        6 items (6 open)
Audit Chain:          INTACT
Audit Events:         2

Reports Generated:    4 PDF reports
```

### Generated PDF Reports

| Report | Size | Contents |
|---|---|---|
| `vendor_dd_VND-OPENAI-2026.pdf` | 18 KB | Risk score, domain breakdown, governance gates, human review, audit trail |
| `dpia_gpt-4o_api_...pdf` | 15 KB | Processing overview, privacy impacts, GDPR articles, recommendations |
| `ai_risk_gpt-4o_api.pdf` | 17 KB | EU AI Act classification, risk factors, governance controls, compliance requirements |
| `integrated_openai_governance_report.pdf` | 13 KB | Combined executive summary — all modules in one board-ready document |

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/anomalyco/trustsphere-ai.git
cd trustsphere-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run all 54 tests
python -m pytest tests/ -v -q

# 4. Run the end-to-end integration verification
python verify.py

# 5. Run the full OpenAI demo
$env:PYTHONIOENCODING='utf-8'; python demo_openai.py   # Windows
# PYTHONIOENCODING=utf-8 python demo_openai.py          # Linux/Mac

# 6. Start the API server + dashboard
python -m src.main review-server --port 8000
# Open http://localhost:8000/dashboard
```

### Dashboard API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/dashboard` | Executive Dashboard (HTML) |
| `GET` | `/api/v1/dashboard/data` | KPI data, vendor/AI distribution, governance |
| `GET` | `/api/v1/dashboard/risks` | Risk register items |
| `GET` | `/api/v1/dashboard/audit` | Audit trail events |
| `POST` | `/api/v1/demo/run-full-assessment` | Run full assessment with sample data |
| `GET` | `/api/v1/review/{vendor_id}` | Get review record |
| `POST` | `/api/v1/review/{vendor_id}/approve` | Approve review |
| `POST` | `/api/v1/review/{vendor_id}/reject` | Reject review (requires reason) |
| `POST` | `/api/v1/review/{vendor_id}/escalate` | Escalate review |
| `POST` | `/api/v1/review/{vendor_id}/request-evidence` | Request more evidence |
| `GET` | `/api/v1/review/pending` | List pending reviews (optional `?role=` filter) |
| `GET` | `/api/v1/audit/{vendor_id}` | Audit events for a vendor |

---

## Comprehensive Use Case: NHS AI Vendor Assessment

An NHS Trust needs to assess a vendor providing an AI-powered clinical decision support system. Here's how TrustSphere AI handles it end-to-end:

### Step 1: Vendor Ingestion
```
Input: Questionnaire data (security, financial, compliance, operational)
Output: Validated vendor profile with risk score
```

### Step 2: Multi-Model Assessment
| Assessment | Output | Regulation |
|---|---|---|
| **Vendor Risk Scoring** | Score: 2.50 (Medium) | NHS DSP Toolkit, ISO 27001 |
| **DPIA** | Overall: HIGH, DPO Required | GDPR Art. 35, UK DPA 2018 |
| **AI Risk Assessment** | Classification: HIGH, Controls: 8 | EU AI Act Annex III |
| **Policy Review** | Coverage: 73%, Gaps: 4 critical | DSP Toolkit, DORA |

### Step 3: Human Review & Approval
```
Risk Analyst → reviews score, requests evidence, escalates to Compliance Officer
Compliance Officer → approves with conditions (mandatory human-in-the-loop)
```

### Step 4: Risk Register
```
6 risks logged (Data Breach, AI Hallucination, Regulatory Noncompliance, Bias...)
Mitigations assigned, owners documented, regulatory references mapped
```

### Step 5: Report Generation
```
4 PDF reports generated → board-ready, audit-ready, regulator-ready
Combined report with executive summary, risk ratings, approval status
```

---

## Compliance Coverage

| Regulation | Vendor DD | AI Risk | DPIA | Policy Review | Risk Register | Audit |
|---|---|---|---|---|---|---|
| **GDPR** | ✓ | ✓ | ✓ ✓ | ✓ | ✓ | ✓ |
| **UK DPA 2018** | | | ✓ | ✓ | | |
| **EU AI Act** | | ✓ ✓ | ✓ | ✓ | | ✓ |
| **NHS DSP Toolkit** | ✓ | ✓ | | ✓ ✓ | | ✓ |
| **ISO 27001** | ✓ | | | ✓ | | ✓ |
| **NIST AI RMF** | | ✓ | | ✓ | | |
| **SOC 2** | ✓ | | | | | ✓ |
| **DORA** | | | | ✓ ✓ | ✓ | ✓ |
| **FCA SYSC 8** | | | | ✓ | ✓ | |
| **SOX** | ✓ | | | ✓ | | ✓ |

---

## Project Structure

```
├── README.md                       # This file
├── MODULES.md                      # Full module documentation
├── ARCHITECTURE.md                 # Detailed data flow and module map
├── PRESENTATION.md                 # Slide deck outline
├── DEMO.md                         # Walkthrough script
├── demo_openai.py                  # End-to-end OpenAI demo script
├── verify.py                       # Integration verification
├── requirements.txt                # Dependencies
│
├── branding/
│   └── logo.svg                    # TrustSphere AI logo
│
├── output/                         # Generated PDF reports
│   ├── vendor_dd_*.pdf
│   ├── dpia_*.pdf
│   ├── ai_risk_*.pdf
│   ├── policy_review_*.pdf
│   └── integrated_*.pdf
│
├── src/
│   ├── main.py                     # CLI + FastAPI server
│   ├── modules/                    # Module registry + 4 modules
│   │   ├── ai_risk_assessment/
│   │   ├── dpia_assessment/
│   │   ├── policy_review/
│   │   └── risk_register/
│   ├── reports/pdf_generator.py    # Professional PDF reports
│   ├── dashboard/templates.py      # Executive dashboard HTML
│   ├── risk_scoring/scorer.py      # 4-domain scoring engine
│   ├── governance/controls.py      # AI governance gates
│   ├── review/approval.py          # Human review lifecycle
│   ├── audit/logger.py             # HMAC hash-chain audit
│   └── questionnaire/intake.py     # Pydantic models + ingestion
│
└── tests/                          # 54 tests across 5 test files
    ├── test_scoring.py
    ├── test_dpia_assessment.py
    ├── test_policy_review.py
    ├── test_ai_risk_assessment.py
    └── test_risk_register.py
```

---

## Skills Demonstrated

| Skill | Evidence |
|---|---|
| **AI Governance** | EU AI Act classification, risk factors, governance controls, human oversight levels |
| **Third-Party Risk Mgmt** | 4-domain scoring, flags, rationale, tier classification |
| **Data Protection** | GDPR Art. 35/36 DPIAs, privacy impacts, DPO consultation, prior authority |
| **Policy Compliance** | Gap analysis against 7 regulatory frameworks, severity scoring |
| **Risk Management** | Inherent/residual risk scoring, heatmap, risk register, mitigations |
| **Human-in-the-Loop** | Role-based routing, SLA, escalation, 2-person override rule |
| **Audit & Evidence** | HMAC-SHA256 hash chain, tamper detection, chain verification |
| **Professional Reporting** | Board-ready PDF generation with executive summaries, tables, KPIs, audit trails |
| **Platform Architecture** | 9-module ecosystem, registry pattern, shared infrastructure, FastAPI |
| **Python Engineering** | Pydantic models, dataclasses, enums, property-based logic, test coverage |

---

## Roadmap

| Phase | Status | Features |
|---|---|---|
| **Phase 1 — Core Engine** | ✅ Complete | Vendor scoring, governance gates, human review, audit chain |
| **Phase 2 — Assessment Modules** | ✅ Complete | DPIA, Policy Review, AI Risk Assessment, Risk Register |
| **Phase 3 — Reporting & Dashboard** | ✅ Complete | PDF reports, executive dashboard, approval workflow UI, API |
| **Phase 4 — Enterprise** | 🔜 Planned | Multi-tenant, SSO, RBAC, database persistence, CI/CD, Terraform |

---

## Why I Built This

I built TrustSphere AI because AI governance, vendor risk, and data protection compliance are the defining regulatory challenges of this decade. The NHS is deploying AI in every department. Banks are integrating with dozens of fintech vendors. Every regulated organisation needs to assess, document, and evidence their AI governance — and most are not equipped to do it at scale.

This project bridges the gap between regulatory theory and practical tooling. It's not a learning exercise — it's a working governance platform that solves real problems for real compliance teams.

---

*Built for organisations that need to reduce risk, improve transparency, and govern AI responsibly.*
