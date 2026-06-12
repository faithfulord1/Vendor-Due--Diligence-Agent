# TrustSphere AI — Architecture

## System Design Overview

TrustSphere AI is a modular governance platform built on a shared infrastructure pattern. Every module shares the same audit layer, human review framework, reporting engine, and module registry.

---

## Data Flow

```
                         ┌──────────────────────────────────┐
                         │        Questionnaire /           │
                         │        Input Data                │
                         └────────────┬─────────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                        INGESTION LAYER                           │
│              Pydantic validation · Schema conformance            │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                     RISK SCORING ENGINE                          │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌───────────┐ │
│  │ Security   │  │ Financial  │  │ Compliance │  │Operational│ │
│  │ (35%)      │  │ (25%)      │  │ (25%)      │  │ (15%)     │ │
│  │ • SOC2     │  │ • Audited  │  │ • GDPR     │  │ • BCP/DR  │ │
│  │ • ISO27001 │  │ • Insur.   │  │ • CCPA     │  │ • Subs    │ │
│  │ • Encrypt  │  │ • Profit   │  │ • HIPAA    │  │ • Crit.   │ │
│  │ • MFA      │  │ • D/E      │  │ • SOX      │  │ • SLA     │ │
│  └────────────┘  └────────────┘  └────────────┘  └───────────┘ │
│                                                                  │
│  Aggregate Score → Risk Tier (Low / Medium / High)              │
│  Elevated Flags → Auto-escalation                               │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    GOVERNANCE GATES                              │
│                                                                  │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────────┐  │
│  │ Input Validation│  │Explainability│  │   Bias Detection    │  │
│  │ • Injections   │  │ • Rationale  │  │ • Population stat   │  │
│  │ • Schema       │  │ • Version    │  │ • Deviation > 2σ    │  │
│  └────────────────┘  └──────────────┘  └─────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                     MODULE ASSESSMENTS                           │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │
│  │   AI Risk        │  │   DPIA           │  │  Policy Review │ │
│  │   Assessment     │  │   Assessment     │  │                │ │
│  │                  │  │                  │  │                │ │
│  │ • EU AI Act      │  │ • GDPR Art. 35  │  │ • Gap analysis │ │
│  │ • Risk factors   │  │ • Privacy impact │  │ • Coverage %   │ │
│  │ • Controls       │  │ • DPO consult   │  │ • Severity     │ │
│  │ • Oversight      │  │ • Prior auth    │  │ • Remediation  │ │
│  └──────────────────┘  └──────────────────┘  └────────────────┘ │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                       RISK REGISTER                              │
│  • Inherent risk score (impact × likelihood)                     │
│  • Residual risk score (after mitigations)                       │
│  • Status: Open / Mitigated / Accepted / Transferred / Closed    │
│  • Heatmap by category                                           │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                  HUMAN-IN-THE-LOOP APPROVAL                      │
│                                                                  │
│  Low Risk ──────► Auto-Approve + Audit Log                       │
│  Medium Risk ───► Risk Analyst Review (48h SLA)                 │
│  High Risk ─────► Compliance Officer Review (24h SLA)           │
│                                                                  │
│  Decisions: Approve · Reject · Re-assess · Override · Escalate  │
│  Controls: Two-person rule for overrides · Evidence requests    │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                       AUDIT LOGGER                               │
│                                                                  │
│  Event ──► HMAC(prev_hash + payload) ──► Hash stored in chain    │
│  verify_chain() recomputes all hashes from genesis to tip        │
│  Tampering with any event breaks the chain                       │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                OUTPUT LAYER                                      │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Executive    │  │ Professional │  │ API (FastAPI)        │   │
│  │ Dashboard   │  │ PDF Reports  │  │ JSON endpoints       │   │
│  │ (HTML/JS)   │  │ (ReportLab)  │  │ for all modules      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Module Registry Pattern

Each module self-registers in `src/modules/__init__.py`:

```python
from src.modules.dpia_assessment import DPIAResult
from src.modules.policy_review import PolicyReviewResult
from src.modules.ai_risk_assessment import AIRiskAssessmentResult
from src.modules.risk_register import RiskRegister

register_module("dpia_assessment", DPIAResult)
register_module("policy_review", PolicyReviewResult)
register_module("ai_risk_assessment", AIRiskAssessmentResult)
register_module("risk_register", RiskRegister)
```

This enables dynamic module discovery, plugin-style extensibility, and clean dependency injection.

---

## Shared Infrastructure

| Component | Location | Purpose |
|---|---|---|
| **Audit Logger** | `src/audit/logger.py` | HMAC-SHA256 tamper-evident hash chain |
| **Human Review** | `src/review/approval.py` | Role-based routing, SLA, escalation, 2-person rule |
| **Module Registry** | `src/modules/__init__.py` | Plugin-style module registration |
| **PDF Reports** | `src/reports/pdf_generator.py` | Professional report generation with ReportLab |
| **Executive Dashboard** | `src/dashboard/templates.py` | Single-page HTML/JS dashboard |
| **n8n Bridge** | `src/n8n_bridge/webhook.py` | Webhook contracts for workflow automation |

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Dataclasses for domain models** | Immutable, type-safe, self-documenting — no ORM overhead for in-memory assessments |
| **Pydantic for ingestion** | Strict validation with error collection, JSON Schema compatibility |
| **Property-based computed fields** | Risk scores, tiers, coverage % are always derived from source data |
| **Enum-based classification** | Type-safe categories, no magic strings, easy serialization |
| **ReportLab for PDFs** | Mature, no system dependencies, precise layout control |
| **HMAC-SHA256 for audit** | Industry-standard tamper evidence, no blockchain overhead |
| **FastAPI for API server** | Type-safe, auto-docs, async ready, industry standard |
| **No database dependency** | In-memory for speed and portability; persistence layer is pluggable |

---

## Test Coverage

| Module | Tests | What's Tested |
|---|---|---|
| Vendor Due Diligence | 14 | Scoring, flags, governance gates, override, human review, audit chain, tamper detection, event filtering |
| DPIA Assessment | 11 | Risk levels, data categories, processing purposes, GDPR articles, recommendations, DPO consultation, prior authority |
| Policy Review | 10 | Coverage %, gap severity, risk score, domain requirements, NHS-specific, banking-specific |
| AI Risk Assessment | 8 | Classification, risk factors, governance controls, summary generation, risk score |
| Risk Register | 11 | Add/get/update, inherent/residual scoring, filtering, summary, NHS examples, banking examples |

**Total: 54 tests, all passing.**
