# Data Architecture: Privacy-First Design

> How we handle user data without actually collecting user data

---

## Core Principle

**We are a calculator, not a financial institution.**

This means:
- No PII required
- No account linking
- No regulatory burden (we don't hold assets or provide advice)
- User owns their data completely

---

## Data We Need vs. Data We DON'T Need

### Required for Calculation (User-Provided)

| Field | Purpose | Stored Where |
|-------|---------|--------------|
| Current savings | Starting point for projection | Client-side only |
| Target amount | Goal to analyze | Client-side only |
| Time horizon | Years to goal | Client-side only |
| Monthly contribution | Savings rate | Client-side only |
| Risk profile | Return/volatility assumptions | Client-side only |
| Monthly income (optional) | Sustainability check | Client-side only |

### NOT Required (We Don't Collect)

| Data Type | Why We Don't Need It |
|-----------|---------------------|
| Name | Not relevant to calculation |
| Email | No account needed |
| Address | Not relevant |
| SSN/Tax ID | We're not a financial institution |
| Actual account balances | User self-reports |
| Investment holdings | We use risk profiles, not specific assets |
| Employer/income details | Only aggregate monthly income |
| Transaction history | Not a budgeting app |

---

## Storage Architecture

### v1: Fully Client-Side

```
┌─────────────────────────────────────────────┐
│                  Browser                     │
│                                              │
│   localStorage                               │
│   ┌────────────────────────────────────┐    │
│   │ {                                  │    │
│   │   "scenarios": [                   │    │
│   │     { "name": "Retire at 65",     │    │
│   │       "inputs": {...},            │    │
│   │       "lastResult": {...}         │    │
│   │     }                              │    │
│   │   ],                               │    │
│   │   "preferences": {                 │    │
│   │     "defaultRiskProfile": "moderate"│   │
│   │   }                                │    │
│   │ }                                  │    │
│   └────────────────────────────────────┘    │
│                                              │
│   IndexedDB (if larger storage needed)       │
│   ┌────────────────────────────────────┐    │
│   │ Historical analyses for comparison  │    │
│   └────────────────────────────────────┘    │
│                                              │
└─────────────────────────────────────────────┘
          │
          │ API calls (stateless)
          ▼
┌─────────────────────────────────────────────┐
│              Server (API)                    │
│                                              │
│   POST /api/analyze                          │
│   • Receives inputs                          │
│   • Runs Monte Carlo                         │
│   • Returns results                          │
│   • NO STATE SAVED                           │
│                                              │
└─────────────────────────────────────────────┘
```

**Benefits:**
- Zero server-side storage = zero data breach risk
- No GDPR/CCPA compliance burden
- User has complete control
- Works offline (if we add service worker)

**Limitations:**
- Data lost if browser cleared
- No cross-device sync
- No server-side analytics

### v1.1: Export/Import for Portability

```json
// Export format (user downloads this file)
{
  "version": "1.0",
  "exportedAt": "2026-01-15T10:30:00Z",
  "scenarios": [
    {
      "name": "Conservative Retirement",
      "created": "2026-01-10",
      "inputs": {
        "currentWealth": 50000,
        "targetWealth": 1000000,
        "yearsToGoal": 30,
        "monthlyContribution": 500,
        "riskProfile": "moderate"
      },
      "lastAnalysis": {
        "probabilityOfSuccess": 0.72,
        "status": "YELLOW",
        "analyzedAt": "2026-01-15"
      }
    }
  ]
}
```

User can:
- Export JSON file
- Import on another device
- Share with advisor
- Version control their planning

### v2: Optional Server Persistence (If Needed)

Only if user validation shows demand for cross-device sync.

**Approach: Anonymous Sessions**

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Browser      │     │      API        │     │    Database     │
│                 │     │                 │     │                 │
│  session_id    ─┼────►│  Validate ID   ─┼────►│  sessions       │
│  (UUID cookie)  │     │                 │     │  ├─ id (UUID)   │
│                 │     │                 │     │  ├─ created_at  │
│                 │     │                 │     │  └─ scenarios[] │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**What we store:**
- Random UUID (not tied to identity)
- Scenario inputs/outputs
- Timestamps

**What we DON'T store:**
- IP addresses (stripped at load balancer)
- Email/name/PII
- Device fingerprints
- Third-party cookies

**Data retention:** Auto-delete after 90 days of inactivity.

---

## Analytics (If Any)

### What We COULD Track (Anonymously)

| Metric | How | Privacy Consideration |
|--------|-----|----------------------|
| Total analyses run | Counter | No user association |
| Distribution of risk profiles | Aggregate only | Never individual |
| Average goal size | Aggregate only | Never individual |
| Status distribution (RED/YELLOW/GREEN) | Aggregate only | General patterns |

### What We Will NOT Track

- Individual user journeys
- Specific financial amounts tied to sessions
- Behavioral patterns per user
- Cross-session user identification

### Implementation: Privacy-Preserving Analytics

```python
# Example: We only send aggregates, never individual data

# BAD - sends user data to analytics
analytics.track("goal_analyzed", {
    "user_id": session_id,  # NO
    "target_amount": 1000000,  # NO
    "current_savings": 50000,  # NO
})

# GOOD - increments aggregate counter only
analytics.increment("analyses_total")
analytics.increment(f"risk_profile_{profile}")  # e.g., "risk_profile_aggressive"
analytics.increment(f"status_{status}")  # e.g., "status_GREEN"
```

---

## Security Considerations

### API Security

| Concern | Mitigation |
|---------|------------|
| DDoS | Rate limiting (100 req/min per IP) |
| Input validation | Pydantic models, bounds checking |
| CORS | Restrict to known origins in production |
| HTTPS | Enforced via infrastructure |

### Client-Side Security

| Concern | Mitigation |
|---------|------------|
| XSS | No user-generated content rendered as HTML |
| localStorage tampering | Data is user's own; no security impact |
| Data exfiltration | Nothing sensitive to exfiltrate |

### What We Don't Need

- Authentication (no accounts)
- Encryption at rest (no sensitive data stored)
- PCI compliance (no payments)
- SOC 2 (no customer data)

---

## Compliance Posture

### GDPR

**Status:** Largely not applicable (no PII collected)

If we add optional email:
- Clear consent at point of collection
- Easy unsubscribe
- Data deletion on request
- No third-party sharing

### CCPA

**Status:** Not applicable (no PII sale)

### Financial Regulations (SEC, FINRA)

**Status:** Not applicable

We are NOT:
- Providing investment advice
- Managing assets
- Recommending specific securities
- Acting as a fiduciary

We ARE:
- A mathematical calculator
- Showing probabilistic projections
- Educational tool only

**Disclaimer (already in UI):**
```
This tool provides educational estimates only and does not constitute 
financial advice. Consult a qualified financial advisor before making 
investment decisions.
```

---

## Data Flow Summary

```
User Input                     Calculation                      Output
    │                              │                              │
    │  currentWealth: 50000        │                              │
    │  targetWealth: 1000000       │                              │
    │  years: 30                   │                              │
    │  monthlyContribution: 500    │   Monte Carlo                │
    │  riskProfile: "aggressive"   │   (20,000 simulations)       │
    │                              │                              │
    ▼                              ▼                              ▼
┌────────────┐               ┌────────────┐               ┌────────────┐
│   Client   │──────────────►│   Server   │──────────────►│   Client   │
│            │   POST        │            │   JSON        │            │
│ (browser)  │   /analyze    │  (stateless)              │  (browser) │
└────────────┘               └────────────┘               └────────────┘
     │                                                          │
     │                                                          │
     ▼                                                          ▼
┌────────────┐                                           ┌────────────┐
│ localStorage│◄──────────────────────────────────────────│ Display    │
│ (optional)  │   User chooses to save                    │ Results    │
└────────────┘                                           └────────────┘
```

**Key property:** Server sees inputs only during request, saves nothing, logs nothing identifiable.

---

## Recommendations

1. **v1:** Stay fully client-side. No database, no analytics.

2. **v1.1:** Add export/import for portability. Still no server storage.

3. **v2 (only if validated):** Anonymous sessions for cross-device sync. Minimal data, auto-expiring.

4. **Never:** PII collection, account linking, third-party data sharing.

---

*End of Data Architecture*
