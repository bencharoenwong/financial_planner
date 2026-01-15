# Financial Goal Analyzer - Product Requirements Document

> **Status:** Draft for review
> **Author:** Chicago Global Capital - Parallax Team
> **Last Updated:** 2026-01-15

---

## Executive Summary

### The Problem

Most people don't do financial planning because:

1. **It's intimidating** - Complex tools assume you know what a "4% safe withdrawal rate" means
2. **It's abstract** - Numbers on a spreadsheet don't feel real
3. **No feedback loop** - You set a goal, then... nothing happens for 30 years
4. **Guilt-inducing** - Tools tell you you're behind, not how to catch up

### The Opportunity

A lightweight financial planning tool that:
- Gives honest, math-based feedback (no AI hallucinations, no sales pitch)
- Makes the first interaction feel achievable, not overwhelming
- Provides ongoing engagement without requiring account management

### Current State

We have a working calculation engine:
- Monte Carlo simulation for goal feasibility
- Risk profile selection (conservative → very aggressive)
- Probability of success with confidence intervals
- Actionable recommendations (increase savings by $X, or adjust target)

**What's missing:** A reason for users to come back. The tool answers "can I reach my goal?" but doesn't help users *engage* with the answer over time.

---

## Target Users

### Primary: "Anxious Planners" (25-45, working professionals)

**Characteristics:**
- Know they should be saving for retirement but haven't done the math
- Intimidated by financial advisors and complex tools
- Want validation or a reality check, not a sales pitch
- Willing to spend 5-10 minutes but not 2 hours

**Jobs to be done:**
- "Am I saving enough for retirement?"
- "What happens if I increase my 401k contribution by 2%?"
- "Is my goal realistic or am I dreaming?"

### Secondary: Financial Advisors (quick client triage)

**Use case:** Rapid feasibility check before detailed planning. Input client's numbers, get RED/YELLOW/GREEN status, share screenshot or PDF.

### Tertiary: Fintech Apps (API integration)

**Use case:** Embed analysis in existing apps. White-label calculation engine.

---

## Product Vision: Two Modes

### Mode 1: Quick Check (No Account Required)

**Flow:**
```
Landing Page → Input Form → Results → Done (or save locally)
```

**User value:** Get an answer in 60 seconds. No signup, no email capture, no friction.

**This exists today.** The current `index.html` does this.

### Mode 2: Engaged Planning (Optional, Lightweight)

**Question:** How do we get users to come back without building a full account system?

**Options evaluated:**

| Approach | Pros | Cons |
|----------|------|------|
| **Local storage only** | No backend, privacy-preserving | Lost if user clears browser |
| **Email-based save** | Simple, no password | Requires email infra |
| **Anonymous ID + cookie** | Persistent, no PII | Still lost on device change |
| **Full accounts** | Best UX | Heavyweight, security burden |

**Recommendation:** Start with **local storage** for v1. Users can save multiple scenarios locally. Export/import as JSON for portability. No backend database required.

---

## Feature Prioritization

### Must Have (v1)

| Feature | Rationale |
|---------|-----------|
| Single goal analysis | Core functionality, already built |
| Clear RED/YELLOW/GREEN status | Instant understanding |
| Specific recommendations | "Increase by $X" not just "save more" |
| Mobile-responsive UI | >50% of users will be on phone |
| No account required | Eliminate friction |

### Should Have (v1.1)

| Feature | Rationale |
|---------|-----------|
| Save/load scenarios (local storage) | Compare options without re-entering |
| Side-by-side comparison | "What if I retire at 60 vs 65?" |
| PDF/image export | Share with spouse, advisor |
| CSV batch upload (API) | Power users, advisors |

### Could Have (v2)

| Feature | Rationale |
|---------|-----------|
| Progress tracking over time | Engagement, habit formation |
| Milestone celebrations | Gamification (hit 50% funded!) |
| Peer comparison (anonymized) | "You're ahead of 60% of similar savers" |
| Multiple linked goals | Retirement + house + college |

### Won't Have (out of scope)

| Feature | Why Not |
|---------|---------|
| Investment recommendations | Regulatory complexity, not our value prop |
| Account aggregation | Plaid integration = complexity + cost |
| Robo-advisor functionality | We're analysis, not management |
| AI-generated advice | Our differentiator is transparency |

---

## Critical Design Questions

### 1. Is gamification right for this product?

**The Duolingo model works because:**
- Language learning requires daily practice
- Progress is measurable (words learned, streak days)
- Social comparison motivates ("your friend finished a lesson")
- Small wins feel achievable

**Financial planning is different:**
- You don't need to check your retirement daily (in fact, you shouldn't)
- Progress is measured in years, not days
- Over-engagement could cause anxiety (checking markets constantly)

**Verdict:** Light gamification only. Progress bars yes, daily streaks no.

### 2. What engagement pattern makes sense?

| Pattern | Fit for Finance |
|---------|-----------------|
| Daily streaks | No - counterproductive |
| Monthly check-ins | Maybe - aligns with pay cycles |
| Milestone celebrations | Yes - "You hit $100k!" |
| What-if scenarios | Yes - exploration is valuable |
| Progress toward goal | Yes - the core feedback loop |

**Recommendation:** Design for **quarterly engagement**, not daily. Prompt users when:
- A milestone is approaching (90% to $100k)
- Market conditions changed significantly
- It's been 3+ months since last check

### 3. What data do we actually need?

**Minimal viable data (stored locally):**
```json
{
  "scenarios": [
    {
      "name": "Retirement at 65",
      "created": "2026-01-15",
      "lastAnalyzed": "2026-01-15",
      "inputs": {
        "currentWealth": 50000,
        "targetWealth": 1000000,
        "yearsToGoal": 30,
        "monthlyContribution": 500,
        "riskProfile": "aggressive"
      },
      "lastResult": {
        "probabilityOfSuccess": 0.72,
        "status": "YELLOW"
      }
    }
  ]
}
```

**We do NOT need:**
- Name, email, phone
- Actual account balances (user self-reports)
- Investment holdings
- Social security number
- Any PII

This is a **calculator**, not a financial institution.

---

## Competitive Positioning

### vs. Wealthfront/Betterment Planning Tools

| Aspect | Them | Us |
|--------|------|-----|
| Business model | Get you to invest with them | No investment product to sell |
| Complexity | Full financial picture | Single-goal focus |
| Account linking | Required (Plaid) | Not needed |
| Trust model | "Trust our robo-advisor" | "Here's the math, you decide" |

**Our advantage:** No conflict of interest. We don't benefit from telling you to invest more.

### vs. Spreadsheet / DIY

| Aspect | DIY | Us |
|--------|-----|-----|
| Accuracy | Depends on your formulas | Monte Carlo simulation built-in |
| Ease | Need to build it yourself | 60 seconds to answer |
| Uncertainty | Usually deterministic | Probabilistic (accounts for volatility) |

**Our advantage:** We've done the math correctly so you don't have to.

### vs. Financial Advisor

| Aspect | Advisor | Us |
|--------|---------|-----|
| Cost | $200-500/hr or 1% AUM | Free |
| Depth | Comprehensive planning | Single-goal feasibility |
| Personalization | High | Limited to inputs |
| Bias | May push products | None |

**Our advantage:** Free reality check before (or instead of) paying for advice.

---

## Success Metrics

### v1 (Launch)

| Metric | Target | Rationale |
|--------|--------|-----------|
| Time to first result | <60 seconds | Frictionless experience |
| Completion rate | >70% | Users finish the analysis |
| Mobile usability score | >90 (Lighthouse) | Works on phones |

### v1.1 (Engagement)

| Metric | Target | Rationale |
|--------|--------|-----------|
| Return visits (30 day) | >20% | Users find it valuable enough to return |
| Scenarios saved | Avg >1.5 per user | Exploring options |
| Share/export rate | >10% | Useful enough to share |

### v2 (Growth)

| Metric | Target | Rationale |
|--------|--------|-----------|
| Monthly active users | Define based on marketing | Adoption |
| API calls | Track | B2B interest |
| NPS | >40 | User satisfaction |

---

## Open Questions for Discussion

1. **Branding:** Is "Chicago Global Capital" the right brand for a consumer tool, or should this be a separate Parallax-branded product?

2. **Monetization path:**
   - Free forever (marketing/brand building)?
   - Freemium (basic free, PDF export paid)?
   - API licensing to fintechs?
   - Lead gen for advisory services?

3. **Depth vs. simplicity trade-off:**
   - Current: Single goal analysis
   - Expansion: Multiple goals, tax optimization, Social Security integration
   - Risk: Feature creep kills simplicity

4. **Engagement philosophy:**
   - Minimal: Calculator only, no persistent state
   - Light: Local storage scenarios, milestone prompts
   - Full: Accounts, notifications, progress tracking

   Where on this spectrum should we land?

---

## Recommended Next Steps

1. **Validate the core value prop** - Get the current tool in front of 10-20 target users. Do they find the output useful? What questions do they have?

2. **Decide on engagement level** - Is local storage enough, or do we need server-side persistence?

3. **Design the "return visit" trigger** - What brings someone back in 3 months?

4. **Technical cleanup** - Fix code duplication, add tests, prepare for iteration

---

## Appendix: Technical Feasibility Notes

### What's Already Built
- Monte Carlo simulation engine (Python)
- REST API with FastAPI
- Single-page web frontend
- CLI batch processing tool

### What's Needed for v1.1 (local storage scenarios)
- JavaScript state management (localStorage)
- Scenario CRUD UI
- Export/import JSON

### What's Needed for v2 (server persistence)
- Database (Postgres or SQLite)
- User accounts (or anonymous session IDs)
- API endpoints for save/load

---

*End of PRD*
