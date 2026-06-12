# TrustSphere AI — Demo Walkthrough

## Scenario: OpenAI (GPT-4o API) Vendor Risk Assessment

This walkthrough demonstrates the complete end-to-end assessment pipeline — from vendor data ingestion to professional PDF report generation — using OpenAI's GPT-4o API as the target vendor.

---

## Prerequisites

```bash
pip install -r requirements.txt
python -m pytest tests/ -v -q    # Verify 54 tests pass
python verify.py                  # Verify integration
```

---

## Quick Demo (1 Command)

```bash
$env:PYTHONIOENCODING='utf-8'; python demo_openai.py
```

This runs the complete pipeline and generates 4 PDF reports in `output/`.

---

## Step-by-Step Walkthrough

### 1. Running the API Server

```bash
python -m src.main review-server --port 8000
```

Opens on `http://localhost:8000/dashboard`.

#### Dashboard Endpoints

| Endpoint | Description |
|---|---|
| `GET /dashboard` | Executive Dashboard (HTML) |
| `GET /api/v1/dashboard/data` | KPI data, vendor/AI distribution, governance |
| `GET /api/v1/dashboard/risks` | Risk register items |
| `GET /api/v1/dashboard/audit` | Audit trail events |

#### Approval Workflow Endpoints

| Method | Endpoint | Body |
|---|---|---|
| `POST` | `/api/v1/review/{vid}/approve` | `{"analyst_id":"...","comments":"..."}` |
| `POST` | `/api/v1/review/{vid}/reject` | `{"analyst_id":"...","reason":"Missing evidence"}` |
| `POST` | `/api/v1/review/{vid}/escalate` | `{"analyst_id":"...","reason":"Complex case"}` |
| `POST` | `/api/v1/review/{vid}/request-evidence` | `{"requested_by":"...","request":"SOC2 report"}` |
| `GET` | `/api/v1/review/pending?role=risk_analyst` | List pending reviews |

### 2. Full Assessment via API

```bash
curl -X POST http://localhost:8000/api/v1/demo/run-full-assessment \
  -H "Content-Type: application/json" \
  -d '{"vendor_name":"NHS Supplier Co","jurisdiction":"UK"}'
```

Returns JSON with scores, assessments, risk register, and PDF file paths.

---

## Demo Script Output (OpenAI)

### [1/9] Vendor Ingestion

```
Vendor:       OpenAI (OpenAI, Inc.)
Jurisdiction: United States (Delaware)
Founded:      2015
Revenue:      $3,700,000,000
```

### [2/9] Risk Scoring

```
Aggregate Score: 1.20/5.00
Risk Tier:       Low
Elevated Flags:  ['not_profitable']

  Security      1.00  No concerns identified
  Financial     1.50  not_profitable
  Compliance    1.00  No concerns identified
  Operational   1.50  No concerns identified
```

### [3/9] Governance Gates

```
input_validation     PASS   All input checks passed
explainability       PASS   All 4 domains have rationales
bias_check           PASS   Bias check passed
```

### [4/9] Audit Trail

```
Events logged:      2
Chain intact:       True
```

### [5/9] Human Review

```
Status:             APPROVED
Final Score:        2.50
Assigned Role:      risk_analyst
Decision:           APPROVE (compliance_lead)
Notes:              "All controls verified. Vendor meets NHS DSP Toolkit standards."
```

### [6/9] DPIA Assessment

```
Overall Risk:       HIGH
Impacts Assessed:   6
DPO Consultation:   Required
Prior Authority:    Required
GDPR Articles:      12
Recommendations:    9
```

Key impacts identified:
- **PSEUDONYMOUS data**: Processing of pseudonymous data — verify anonymisation
- **AI_TRAINING purpose**: AI training with personal data — high risk of re-identification
- **International transfer**: Transfer to third country without adequacy decision
- **Automated decision-making**: GDPR Art. 22 safeguards required
- **Vulnerable subjects**: Additional protections required

### [7/9] AI Risk Assessment (EU AI Act)

```
Risk Category:      UNACCEPTABLE
Risk Score:         5/5
Risk Factors:       4 present
Controls Required:  0 (unacceptable — do not deploy)
Requires DPIA:      True
Human Review:       Required
Oversight:          Human In Command
```

Risk factors detected:
1. **Healthcare Diagnosis** — High-risk under EU AI Act Annex III
2. **Sensitive Data** — Special category data processing
3. **Vulnerable Groups** — Additional protections required
4. **Profiling** — Systematic profiling of individuals

### [8/9] Risk Register

```
Total Risks:        6
Open:               6
Critical:           1
High:               4
Avg Inherent:       13.7
```

| ID | Category | Rating | Status |
|---|---|---|---|---|
| RISK-0001 | Data Breach | HIGH | Open |
| RISK-0002 | AI Hallucination | HIGH | Open |
| RISK-0003 | Regulatory Noncompliance | HIGH | Open |
| RISK-0004 | Bias Discrimination | HIGH | Open |
| RISK-0005 | Third-Party Failure | MEDIUM | Open |
| RISK-0006 | Cyber Attack | CRITICAL | Open |

### [9/9] PDF Reports Generated

```
[ 18 KB] Vendor Due Diligence      vendor_dd_VND-OPENAI-2026.pdf
[ 15 KB] DPIA Assessment           dpia_gpt-4o_api_....pdf
[ 17 KB] AI Risk Assessment        ai_risk_gpt-4o_api.pdf
[ 13 KB] Integrated Governance     integrated_openai_governance_report.pdf
```

---

## Sample API Usage

### Ingest and Score a Vendor

```python
from src.questionnaire.intake import ingest_from_dict
from src.risk_scoring.scorer import score_questionnaire

data = {
    "supplier": {"name": "Acme AI Ltd", "legal_entity": "Acme Inc",
                 "jurisdiction": "UK", "year_founded": 2018},
    "security": {"has_soc2": True, "has_iso27001": False, "mfa_enforced": True},
    "financial": {"audited_financials_available": True, "profitable_last_3_years": True},
    "compliance": {"gdpr_compliant": True, "hipaa_compliant": False},
    "operational": {"bcp_dr_plan_exists": True, "critical_vendor": False},
}

intake = ingest_from_dict(data)
card = score_questionnaire(intake.questionnaire)
print(f"Aggregate: {card.aggregate_score:.2f}, Tier: {card.risk_tier.value}")
```

### Run a DPIA

```python
from src.modules.dpia_assessment import DPIARequest, DataCategory, ProcessingPurpose, assess_dpia

req = DPIARequest(
    title="Patient Data AI Triage",
    controller="NHS Trust",
    processing_purpose=ProcessingPurpose.HEALTH,
    data_categories=[DataCategory.SPECIAL_CATEGORY],
    automated_decision_making=True,
)
result = assess_dpia(req)
print(f"DPIA Risk: {result.overall_risk.value}, DPO: {result.dpo_consultation_required}")
```

### Classify an AI System

```python
from src.modules.ai_risk_assessment import AIAssessmentRequest, AIDomain, assess_ai_risk

req = AIAssessmentRequest(
    system_name="Diagnostic AI",
    domain=AIDomain.HEALTHCARE,
    description="AI-powered radiology assistant",
    used_in_healthcare_diagnosis=True,
)
result = assess_ai_risk(req)
print(f"EU AI Act Class: {result.risk_category.value}, Score: {result.risk_score}/5")
```

---

## Tests

```bash
# Run all 54 tests
python -m pytest tests/ -v

# Run specific modules
python -m pytest tests/test_scoring.py -v              # Vendor scoring (14 tests)
python -m pytest tests/test_dpia_assessment.py -v       # DPIA (11 tests)
python -m pytest tests/test_policy_review.py -v         # Policy review (10 tests)
python -m pytest tests/test_ai_risk_assessment.py -v    # AI risk (8 tests)
python -m pytest tests/test_risk_register.py -v         # Risk register (11 tests)

# Integration verification
python verify.py
```
