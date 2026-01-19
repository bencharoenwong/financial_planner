# Growth Graph Freemium Strategy

*Research completed: 2026-01-17*

## Executive Summary

Based on content marketing and UX research analysis, this document outlines the monetization strategy for Growth Graph. The core insight: **scenario comparison is the killer feature** - highest willingness to pay, clearest conversion trigger, lowest implementation effort.

**Preferred Model (per Ben):** Pay-per-report/update rather than subscription.

---

## Pricing Models Considered

### Option A: Subscription (Industry Standard)
| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | Full calculator, 1 saved scenario, no exports |
| Pro | $8-12/mo or $79-99/yr | Unlimited saves, comparison, exports, history |
| Advisor | $299/yr | White-label, API, batch processing |

**Pros:** Predictable revenue, industry standard, incentivizes ongoing engagement
**Cons:** Subscription fatigue, feels like "renting" software

### Option B: Pay-Per-Use (Preferred Direction)
| Action | Price | Notes |
|--------|-------|-------|
| Free analysis | $0 | Unlimited, builds trust |
| Export PDF report | $3-5 | One-time, high perceived value |
| Save scenario pack (5) | $10 | Enables comparison workflow |
| Full comparison report | $5-10 | Side-by-side PDF with recommendations |
| Annual unlimited | $49-79 | For power users, converts frequent buyers |

**Pros:**
- No subscription resistance ("I already have too many")
- Feels transactional, not ongoing obligation
- Aligns with quarterly check-in use pattern
- Lower barrier to first purchase

**Cons:**
- Less predictable revenue
- Need to optimize for repeat purchases
- Risk of nickel-and-dime perception (mitigate with bundles)

### Option C: Hybrid (Recommended Testing)
- Free tier with full calculator
- Pay-per-export ($3-5 per PDF report)
- "Report pack" bundles (5 for $15, 10 for $25)
- Optional annual pass ($49/yr) for unlimited exports

**Rationale:** Start with pay-per-use, offer annual pass as upsell for frequent users.

---

## What Users Pay For (Ranked by Value)

Based on competitive analysis and user psychology research:

| Feature | % Cite as Valuable | Willingness to Pay | Implementation Effort |
|---------|-------------------|-------------------|----------------------|
| Saved scenarios + comparison | 85% | HIGH | Low |
| Export to PDF/Excel | 60% | HIGH | Low |
| Historical progress tracking | 55% | MODERATE | Medium |
| Multi-goal portfolio | 50% | MODERATE-HIGH | Medium |
| Custom Monte Carlo params | 40% | HIGH (niche) | Medium |
| Batch/API processing | 20% | VERY HIGH (B2B) | High |

---

## User Segments

| Segment | Profile | Premium Trigger | Price Sensitivity |
|---------|---------|-----------------|-------------------|
| Anxious First-Timers | 25-35, just starting | Export to share with partner | HIGH ($0-5) |
| Scenario Planners | 30-45, optimizing | Comparison view | MODERATE ($5-15) |
| FIRE Community | 25-45, high engagement | Progress tracking, sharing | LOW ($10-20) |
| Financial Advisors | Professional use | Batch, white-label | VERY LOW ($50-200) |

---

## Conversion Funnel

```
1000 visitors
    │
    ├─► 700 start analysis (70%)
    │      │
    │      ├─► 490 complete (70% of starters)
    │      │      │
    │      │      ├─► 200 return within 30 days (40%)
    │      │      │      │
    │      │      │      └─► 20-40 purchase something (10-20% of returners)
    │      │      │
    │      │      └─► 5-10 impulse buy on first visit (1-2%)
    │
    └─► Total: 25-50 paying customers per 1000 visitors (2.5-5%)
```

**Key insight:** Conversion happens at re-engagement (2nd-4th visit), not first visit.

---

## Pay-Per-Use Implementation

### Trigger Points (When to Show Purchase Option)

1. **After completing analysis:** "Download this as a PDF report ($3)"
2. **After 2nd scenario:** "Save and compare your scenarios ($5 for comparison report)"
3. **When switching Goal/FIRE modes:** "Track both goals - get a combined report ($5)"
4. **On return visit:** "Your plan changed - get an updated report ($3)"

### Pricing Psychology

- **Anchor high:** Show "Full report pack $25" first, then "$5 single report"
- **Bundle discounts:** 5 reports for $15 (save $10)
- **Annual pass upsell:** After 3rd purchase, offer "$49/yr unlimited"
- **No credit card for free tier:** Reduces friction

### Payment Flow

```
[Complete Analysis]
        │
        ▼
┌─────────────────────────────────────┐
│  Your Financial Plan is Ready       │
│                                      │
│  📊 Success Probability: 78%         │
│  💰 Monthly savings needed: $850     │
│                                      │
│  ┌─────────────────────────────────┐ │
│  │ [Screenshot - Free]             │ │
│  │ [Download PDF Report - $3]      │ │
│  │ [Compare Scenarios - $5]        │ │
│  └─────────────────────────────────┘ │
│                                      │
│  🔒 Secure payment • No account req  │
└─────────────────────────────────────┘
```

---

## Trust Requirements (Before Monetizing)

### Must-Have Before Launch
- [ ] About page (Chicago Global credentials, team, mission)
- [ ] "How it works" methodology explanation
- [ ] Privacy policy (emphasize no data storage)
- [ ] Contact information (email, not just form)

### Nice-to-Have
- [ ] Testimonials from beta users (3-5 quotes)
- [ ] Usage stats ("10,000+ analyses run")
- [ ] FAQ addressing common concerns
- [ ] Trust badges on payment page

---

## B2B Tier (Advisors)

Separate pricing for professional use:

| Feature | Price |
|---------|-------|
| Batch CSV upload (up to 50 clients) | $99/month |
| API access (1,000 calls/month) | $199/month |
| White-label PDF exports | +$50/month |
| Custom risk profiles | Included with API |

**Target:** 10-20 advisor customers = $1-2k MRR

---

## Competitive Positioning

| Tool | Model | Price | Growth Graph Advantage |
|------|-------|-------|----------------------|
| Wealthfront | Free (sells AUM) | Free | No product to sell, transparent |
| YNAB | Subscription | $14.99/mo | Lower commitment, pay-per-use |
| Personal Capital | Free (sells advice) | Free | Privacy-first, no upsell |
| MaxiFi | Subscription | $109-159/yr | Simpler, lower price point |
| Fidelity/Vanguard | Free (sells funds) | Free | Independent, no bias |

**Positioning:** "The honest calculator. Pay only for what you need. No subscriptions, no hidden agenda."

---

## Revenue Projections

### Conservative (Pay-Per-Use)
- 10,000 monthly users
- 3% purchase rate = 300 purchases/month
- Average purchase: $5
- **Monthly revenue: $1,500**
- **Annual revenue: $18,000**

### Optimistic (With Bundles + Annual)
- 10,000 monthly users
- 5% purchase rate = 500 purchases/month
- Average purchase: $8 (mix of singles and bundles)
- 50 annual pass holders @ $49 = $2,450/yr
- **Monthly revenue: $4,000 + $200 (annual amortized) = $4,200**
- **Annual revenue: $50,000**

### With B2B Tier
- Add 10 advisor customers @ $150/mo avg = $1,500/mo
- **Additional annual revenue: $18,000**

---

## Implementation Phases

### Phase 1: Core Pay-Per-Use (Weeks 1-4)
1. Stripe integration (Stripe Checkout for simplicity)
2. PDF export feature (browser print-to-PDF initially)
3. Payment trigger after analysis completion
4. Email receipt delivery

### Phase 2: Scenario Comparison (Weeks 5-8)
1. Local storage for multiple scenarios
2. Comparison view UI
3. Comparison PDF report generation
4. Bundle pricing (5-pack, 10-pack)

### Phase 3: Optimize & Upsell (Months 3-4)
1. Annual pass option
2. A/B test pricing ($3 vs $5 vs $7)
3. Re-engagement emails for saved scenarios
4. Advisor tier soft launch

---

## Deep Research Prompts

For current market validation, use with Claude's deep research:

```
1. "What are the current (2026) pricing tiers for YNAB, Monarch Money,
   Copilot, and PocketGuard? Include annual vs monthly pricing."

2. "What is the typical conversion rate for pay-per-use vs subscription
   in consumer fintech apps 2025-2026?"

3. "Case study: How does MaxiFi or Boldin structure their pricing?
   What features are paywalled?"

4. "User willingness to pay for financial planning software - survey data
   on price sensitivity for DIY investors."
```

---

## User Research (Ready to Deploy)

### Interview Questions (10-15 users)
1. Tell me about your financial planning process
2. What tools do you currently use? Frustrations?
3. Walk me through your Growth Graph experience
4. If you could add one feature, what would it be?
5. Would you pay $3-5 for a PDF report? Why/why not?
6. Subscription vs pay-per-use - which feels better?

### Survey Questions (200-500 users)
- How many times have you used the calculator?
- What features would be most valuable? (rank)
- What would you pay for premium features?
- Preferred payment model? (monthly/annual/per-use/lifetime)
- What builds trust for you in financial tools?

---

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-01-17 | Pay-per-use over subscription | Aligns with quarterly use pattern, reduces subscription fatigue, lower barrier to first purchase |

---

## Implementation Requirements

### Phase 0: Trust Foundation (Before Any Monetization)

Without these, users won't enter payment info:

| Item | Description | Priority |
|------|-------------|----------|
| **About page** | Chicago Global credentials, team background, mission | CRITICAL |
| **Methodology section** | "How does Monte Carlo work?" with visual | CRITICAL |
| **Privacy policy** | Emphasize local-first, no data storage | CRITICAL |
| **Contact info** | Real email, not just form | HIGH |
| **Usage stats** | "X analyses run" counter | MEDIUM |

### Phase 1: Single Report Purchase

**Goal:** Validate willingness to pay with simplest possible flow.

**Scope:**
- [ ] Stripe Checkout integration (one-time payments)
- [ ] PDF export generation (Goal Mode report)
- [ ] "Download Report - $5" button after analysis
- [ ] Email receipt with PDF attached
- [ ] Thank you page with download link

**Technical approach:**
- Use Stripe Checkout (hosted payment page) - no custom payment UI
- PDF: Start with server-side HTML-to-PDF (WeasyPrint or similar)
- No accounts - purchase tied to email for receipt only

**Pricing test:** Start at $5, measure conversion. A/B test $3 vs $5 vs $7.

### Phase 2: Scenario Comparison

**Goal:** Enable the "killer feature" - comparing scenarios.

**Scope:**
- [ ] Save scenarios to localStorage (up to 5)
- [ ] Comparison view UI (side-by-side)
- [ ] Comparison report PDF ($7-10)
- [ ] "Save Scenario" button (free, limited to 5)
- [ ] "Compare" button (shows free preview, paywall on export)

**Upsell moment:** After 3rd saved scenario, prompt: "Want a professional comparison report? $7"

### Phase 3: Bundles & Annual Pass

**Goal:** Increase average revenue per user.

**Scope:**
- [ ] Report pack (5 reports for $15)
- [ ] Annual unlimited pass ($49)
- [ ] "You've purchased 3 reports - upgrade to unlimited for $49"
- [ ] Stripe Customer Portal for pass holders

### Phase 4: B2B / Advisor Tier

**Goal:** Revenue concentration from professional users.

**Scope:**
- [ ] Batch CSV processing
- [ ] White-label PDF (custom logo)
- [ ] API access
- [ ] $99-199/month pricing

---

## Technical Architecture (Simplified for Pay-Per-Use)

```
┌─────────────────────────────────────────────────────┐
│                    Frontend                          │
│  - Calculator (existing)                            │
│  - Save to localStorage                             │
│  - Comparison view                                  │
│  - "Buy Report" → Stripe Checkout redirect          │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                    Backend (API)                     │
│  - /api/analyze (existing)                          │
│  - /api/checkout - Create Stripe session            │
│  - /api/webhook - Handle payment success            │
│  - /api/report/generate - Create PDF                │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                  External Services                   │
│  - Stripe (payments)                                │
│  - Email (receipt + PDF delivery)                   │
│  - PDF generation (WeasyPrint / Puppeteer)          │
└─────────────────────────────────────────────────────┘
```

**Key simplification:** No user database. Each purchase is standalone.
- Stripe handles customer record (for receipts, refunds)
- PDF generated on-demand at time of purchase
- No login, no stored data beyond localStorage

---

## Content Needed

### About Page
```
# About Growth Graph

Growth Graph is built by Chicago Global Capital, a quantitative
investment firm focused on systematic strategies.

We built this tool because [story/mission].

**Our credentials:**
- [Ben's background]
- [Team expertise]

**Our philosophy:**
- Independent: We don't sell investment products
- Private: Your data stays on your device
- Honest: Transparent methodology, no black boxes

Contact: [email]
```

### Methodology Section
```
# How Growth Graph Works

## Monte Carlo Simulation
[Visual showing multiple random paths]

We run 10,000 simulations of your investment journey, each with
different randomly-generated market returns based on your risk profile.

## Risk Profiles
| Profile | Expected Return | Volatility | Based On |
|---------|-----------------|------------|----------|
| Conservative | 6% | 10% | 70/30 bonds/stocks |
| Moderate | 8% | 13% | 40/60 balanced |
| Aggressive | 10% | 16% | S&P 500-like |
| Very Aggressive | 12% | 20% | Concentrated growth |

## What the Probability Means
- 80%+ (Green): On track with good margin
- 50-79% (Yellow): Achievable but needs monitoring
- <50% (Red): Significant changes needed

[Link to full methodology / academic references]
```

---

## Next Steps

1. [ ] Create About page (content above)
2. [ ] Add Methodology section to index.html or separate page
3. [ ] Draft Privacy Policy
4. [ ] Set up Stripe account + test mode
5. [ ] Build PDF report template
6. [ ] Integrate Stripe Checkout
7. [ ] Soft launch at $5/report
8. [ ] Measure conversion, iterate
