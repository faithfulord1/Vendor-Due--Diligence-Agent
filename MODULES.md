# TrustSphere AI — Module Architecture

## Enterprise AI Governance, Risk, Compliance and Third-Party Risk Management Platform

---

## Overview

TrustSphere AI is a nine-module governance platform. Each module addresses a specific governance domain while sharing a common audit trail, human-in-the-loop framework, professional PDF reporting, and executive dashboard.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TRUSTSPHERE AI PLATFORM                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Vendor Due   │  │ Risk Register│  │ AI Risk Assessment       │  │
│  │ Diligence    │  │              │  │                          │  │
│  ├──────────────┤  ├──────────────┤  ├──────────────────────────┤  │
│  │ • Scoring    │  │ • Inherent/  │  │ • EU AI Act class.       │  │
│  │ • Flags      │  │   residual   │  │ • Risk factors           │  │
│  │ • Domains    │  │ • Heatmap    │  │ • Governance controls    │  │
│  │ • Rationale  │  │ • Summary    │  │ • Human oversight        │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Policy Review│  │ DPIA         │  │ Audit & Evidence         │  │
│  │              │  │ Assessment   │  │ Management               │  │
│  ├──────────────┤  ├──────────────┤  ├──────────────────────────┤  │
│  │ • Gap ID     │  │ • GDPR Art.  │  │ • HMAC-SHA256 chain      │  │
│  │ • Coverage % │  │ • Impacts    │  │ • Tamper detection       │  │
│  │ • Severity   │  │ • DPO req.   │  │ • Event filtering        │  │
│  │ • Compliance │  │ • Prior auth │  │ • JSONL export           │  │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────┐  ┌──────────────────────────┐  │
│  │ Human-in-the-Loop Approval   │  │ Professional PDF         │  │
│  │ Framework                    │  │ Reports                  │  │
│  ├──────────────────────────────┤  ├──────────────────────────┤  │
│  │ • Role-based assignment      │  │ • Vendor DD Report       │  │
│  │ • SLA enforcement            │  │ • AI Risk Report         │  │
│  │ • Escalation                 │  │ • DPIA Report            │  │
│  │ • 2-person rule for override │  │ • Policy Review Report   │  │
│  └──────────────────────────────┘  │ • Combined Governance    │  │
│                                     └──────────────────────────┘  │
│                                                                     │
│  ┌──────────────────────────────────────┐                           │
│  │ Executive Dashboard                   │                           │
│  ├──────────────────────────────────────┤                           │
│  │ • KPI cards  • Risk register table   │                           │
│  │ • Heatmap    • Vendor/AI distribution │                           │
│  │ • Governance • Audit trail summary   │                           │
│  │   status                             │                           │
│  └──────────────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘
```

## Module Inventory

| # | Module | Status | Tests | Business Function | Industry Relevance |
|---|---|---|---|---|---|
| 1 | Vendor Due Diligence | **Complete** | 14 | Vendor onboarding, scoring, flags, rationale | NHS, Banking, Gov, Insurance, Tech |
| 2 | Risk Register | **Complete** | 11 | Inherent/residual scoring, heatmap, summary | All regulated sectors |
| 3 | AI Risk Assessment | **Complete** | 8 | EU AI Act classification, risk factors, controls | NHS, Banking, Gov, Tech |
| 4 | Policy Review | **Complete** | 10 | Gap analysis, coverage %, severity, NHS/Banking | NHS, Gov, Insurance |
| 5 | DPIA Assessment | **Complete** | 11 | Data protection, GDPR Art. 35/36, DPO | NHS, Banking, Gov, Insurance |
| 6 | Audit & Evidence | **Complete** | 3 | HMAC-SHA256 chain, tamper detection, filtering | All regulated sectors |
| 7 | Human-in-the-Loop | **Complete** | 3 | Approval routing, SLA, escalation, 2-person | All regulated sectors |
| 8 | Executive Dashboard | **Complete** | — | KPI cards, risk table, heatmap, audit trail | Board, C-suite, Audit Committee |
| 9 | Professional PDF Reports | **Complete** | — | Vendor DD, AI Risk, DPIA, Policy, Combined | All regulated sectors |

**Total: 54 tests, all passing.**

## Module Dependency Map

```
                    ┌──────────────────────────┐
                    │   Executive Dashboard    │
                    │   Professional Reports   │
                    └────────┬────────┬────────┘
                             │        │
          ┌──────────────────┼────────┼──────────────────┐
          │                  │        │                  │
          ▼                  ▼        ▼                  ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Vendor Due        │ │ AI Risk      │ │ DPIA         │ │ Policy       │
│ Diligence         │ │ Assessment   │ │ Assessment   │ │ Review       │
└────────┬─────────┘ └────────┬─────┘ └────────┬─────┘ └────────┬─────┘
         │                    │                │               │
         ▼                    ▼                ▼               ▼
┌──────────────────────────────────────────────────────────────────┐
│                    Risk Register                                  │
│              (inherent / residual scoring)                        │
└────────────────────────────────┬─────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│           Human-in-the-Loop Approval Framework                    │
│        (Common governance layer with SLA enforcement)            │
└──────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│           Audit Logger (HMAC-SHA256 tamper-evident chain)        │
└──────────────────────────────────────────────────────────────────┘
```

## Shared Infrastructure

All modules share:

| Component | Description |
|---|---|
| **Audit Logger** | HMAC-SHA256 hash chain — tamper-evident, verifiable |
| **Human Review** | Role-based approval routing with SLA enforcement |
| **n8n Bridge** | Webhook contracts for Slack, email, ERP integration |
| **Export Layer** | JSONL, CSV, PDF output formats (PDF via reportlab) |
| **Schema Contracts** | Pydantic validation across all modules |
| **Module Registry** | Plugin-style module registration in `src/modules/` |
| **Reports** | Professional PDF generation in `src/reports/` |

## Regulatory Coverage by Module

| Regulation | Modules |
|---|---|
| **GDPR** | Vendor Due Diligence, AI Risk, DPIA, Policy Review, Audit |
| **UK DPA 2018** | DPIA, Policy Review, Audit |
| **EU AI Act** | AI Risk, DPIA, Policy Review, Human-in-the-Loop |
| **NHS DSP Toolkit** | Vendor Due Diligence, AI Risk, Policy Review, Audit |
| **ISO 27001** | Vendor Due Diligence, Policy Review, Audit |
| **NIST AI RMF** | AI Risk, Policy Review |
| **SOC 2** | Vendor Due Diligence, Audit |
| **DORA** | Policy Review (ICT risk, third-party), Risk Register |
| **FCA SYSC 8** | Policy Review (outsourcing), Risk Register |
| **SOX** | Policy Review, Vendor Due Diligence |

## Module Lifecycle

| Phase | Description |
|---|---|
| **Spec** | Requirements documented, no implementation yet |
| **Stub** | Minimal implementation with module interface, models, and placeholders |
| **Complete** | Full implementation with tests and documentation |

## Adding a New Module

Each module should:
1. Live in `src/modules/<module_name>/`
2. Expose a public interface via `ModuleRegistry`
3. Use shared infrastructure (audit, review, reports)
4. Register in `src/modules/__init__.py`
