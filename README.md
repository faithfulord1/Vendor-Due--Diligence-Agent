# TrustSphere Vendor Due Diligence Agent

**Explainable third-party risk triage with human-governed decisions**

TrustSphere is a portfolio-grade TPRM service that converts a structured vendor questionnaire into transparent risk findings, evidence requests and a human-review decision path.

> **Design principle:** the engine can identify risk and prepare evidence. An authorised person remains responsible for vendor approval, rejection and onboarding.

## Why this project exists

Vendor reviews often arrive as spreadsheets, email chains and inconsistent checklists. TrustSphere demonstrates a simpler controlled flow:

1. collect a small set of vendor control facts
2. apply deterministic, inspectable rules
3. generate stable control IDs and evidence requests
4. escalate higher-risk or critical vendors for human review
5. preserve the reasoning behind the result

### Real-life example

An NHS supplier will process patient information and is considered business-critical. The questionnaire says MFA is not enforced, disaster recovery has not been tested this year and the supplier had a recent security incident.

TrustSphere does not simply label the company “bad”. It returns concrete findings such as `TPRM-SEC-001`, `TPRM-IAM-001` and `TPRM-RES-001`, explains what evidence is missing and marks human review as required. A compliance officer then decides what happens next.

## Working API

The current runnable service is implemented in `main.py` using FastAPI.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

### Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/` | project status and purpose |
| GET | `/health` | health check |
| POST | `/assess` | deterministic vendor-risk assessment |

Example assessment body:

```json
{
  "vendor_name": "Critical Health Processor",
  "critical_vendor": true,
  "handles_personal_data": true,
  "handles_special_category_data": true,
  "mfa_enforced": false,
  "encryption_at_rest": true,
  "encryption_in_transit": false,
  "bcp_tested_last_12_months": false,
  "breach_last_12_months": true
}
```

The response includes a risk score, tier, stable control findings, evidence requirements, critical blockers and whether human review is required.

## Current deterministic controls

- `TPRM-SAN-001` sanctions / PEP escalation
- `TPRM-REG-001` active regulatory investigation
- `TPRM-SEC-001` recent security incident
- `TPRM-IAM-001` MFA assurance
- `TPRM-ENC-001` encryption assurance
- `TPRM-RES-001` resilience / BCP testing
- `TPRM-ASS-001` independent security assurance
- `TPRM-DPIA-001` higher privacy impact for special-category data

The rules are intentionally visible. This makes the project easier to test, explain and govern than a hidden “AI score”.

## Verification

```bash
python verify.py
```

The verifier checks low-risk, high-risk and sanctions-escalation scenarios. GitHub Actions runs these checks and confirms that the FastAPI application imports correctly on every push and pull request.

## Repository notes

Earlier documentation and demo files described a larger nine-module TrustSphere prototype. Some of those source modules were not present in this GitHub repository, so the public README previously overstated what a visitor could actually run. This hardening pass fixes that gap by making the repository truthfully runnable today.

Historical design documents such as `ARCHITECTURE.md`, `MODULES.md`, `PRESENTATION.md` and `DEMO.md` remain useful as roadmap material. `demo_openai.py` is retained as historical prototype material and should not be treated as the verified entry point until its legacy module dependencies are restored.

## Security and governance boundaries

- questionnaire inputs should not contain unnecessary personal data
- sanctions or regulatory flags are signals for authorised review, not automatic legal conclusions
- vendor approval and onboarding remain human decisions
- production use needs authentication, RBAC, durable audit storage, encryption, retention controls and approved external screening sources
- never place API keys or confidential vendor evidence in the public repository

## Portfolio direction

The next sensible extension is a governed MCP layer that exposes read-only assessment and evidence-explanation tools to an AI client while keeping vendor approval outside the agent tool surface.

Built by **Faith Wright** as part of the Palm92 Intelligence governance portfolio.

## License

MIT. See `LICENSE`.
