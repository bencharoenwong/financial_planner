# Product Roadmap: Financial Goal Analyzer

## Vision

**Independent, international, privacy-first financial planning tools.**

We help globally mobile professionals (expats, MBA students, remote workers) make informed financial decisions without selling them products or harvesting their data.

---

## Freemium Model

### Tier Structure

| Tier | Price | Target User | Core Value |
|------|-------|-------------|------------|
| **Free** | $0 | Curious → Planning | Education + basic analysis |
| **Pro** | $49/year | Serious planners | Customization + scenarios |
| **Premium** | $149/year | Optimizers | Tax intelligence + reports |

### What Stays Free (Forever)

The educational core that builds trust:

- Monte Carlo calculator (Goal Mode + FIRE Mode)
- Standard risk profiles (conservative/moderate/aggressive/very aggressive)
- Success probability, percentiles, required contribution
- Framework wizard with LLM prompts
- Single goal analysis at a time
- Basic charts and visualizations
- Local storage for one saved scenario
- Full offline functionality

**Philosophy:** Free users should be able to build a solid financial plan. Premium helps them optimize it.

### Pro Tier ($49/year or $5/month)

For users who want more control:

**Custom Portfolios**
- Define your own asset allocation (not just risk profiles)
- Set custom return/volatility assumptions
- Model specific fund combinations (e.g., 60% VTI, 30% VXUS, 10% BND)

**Multi-Goal Planning**
- Track unlimited goals simultaneously
- See aggregate savings requirements
- Prioritization recommendations (which goal to fund first?)

**Scenario Comparison**
- Side-by-side "what if" analysis
- Compare 2-4 scenarios on same screen
- Sensitivity analysis (how much does X assumption matter?)

**Advanced Withdrawal Strategies**
- Variable percentage withdrawal (Guyton-Klinger guardrails)
- CAPE-based dynamic withdrawal
- Floor-and-ceiling approaches
- Bond tent / rising equity glidepath

**Historical Backtesting**
- "What if I retired in 2000?" stress tests
- Sequence of returns analysis with real historical data
- Best/worst case historical scenarios

### Premium Tier ($149/year or $15/month)

For serious optimizers and cross-border situations:

**Tax Intelligence Modules**
- Country-specific after-tax return modeling
- Tax-advantaged vs taxable account optimization
- Effective tax rate calculations by account type
- Roth conversion analysis (US)
- ISA/SIPP optimization (UK)
- CPF/SRS modeling (Singapore)
- PEA/Assurance Vie (France)

**Cross-Border Planning**
- "What if I move from X to Y?" scenario comparison
- Tax treaty impact analysis
- Portability scores for different account types
- Dual-tax situation modeling

**Professional Reports**
- PDF export with full analysis
- Executive summary for advisors/partners
- Printable one-page plan summary
- Detailed methodology appendix

**MCP Integration**
- Use calculator directly from Claude/ChatGPT
- Natural language goal input
- Conversational scenario exploration

**API Access**
- Programmatic access for developers
- Webhook notifications for plan reviews
- Integration with other tools

---

## Development Phases

### Phase 1: Foundation (Complete)

✅ Monte Carlo simulation engine
✅ Goal Mode + FIRE Mode calculators
✅ REST API
✅ Web frontend
✅ Framework wizard with LLM prompts
✅ Basic visualizations

### Phase 2: Enhanced Free Tier (Next)

**Goals:** Increase engagement, establish habit, create upgrade moments

- [ ] **Multi-goal tracking (limited)** - Save up to 3 goals, see combined view
- [ ] **Improved visualizations** - Better charts, mobile-responsive
- [ ] **Local storage** - Browser-based save/load (no account needed)
- [ ] **Comparison view** - See two scenarios side by side
- [ ] **Export to JSON** - Download your data, import later
- [ ] **Sharing** - Generate shareable link (privacy-preserving, no PII)

**Upgrade trigger:** "Want to save more than 3 goals? Upgrade to Pro"

### Phase 3: Pro Tier Launch

**Goals:** Convert serious users, validate willingness to pay

- [ ] **User accounts** - Simple auth (magic links or OAuth)
- [ ] **Custom portfolio builder** - Define your own allocation
- [ ] **Unlimited goals** - No cap on saved scenarios
- [ ] **Advanced withdrawal strategies** - Guardrails, CAPE-based, etc.
- [ ] **Scenario comparison** - Side-by-side analysis
- [ ] **Historical backtesting** - Real market data integration
- [ ] **Payment integration** - Stripe for subscriptions

**Technical requirements:**
- Authentication system
- Encrypted user data storage (scenarios only, not PII)
- Feature flag system
- Stripe integration

### Phase 4: Premium Tier / Tax Intelligence

**Goals:** Serve high-value users, differentiate from competitors

- [ ] **Country tax modules** - Start with 5 key markets:
  - United States (401k, IRA, Roth, HSA, capital gains)
  - United Kingdom (ISA, SIPP, pension, CGT)
  - Singapore (CPF, SRS, no capital gains)
  - France (PEA, Assurance Vie, PER)
  - Germany (Riester, company pension, Abgeltungsteuer)
- [ ] **After-tax projections** - Model actual take-home growth
- [ ] **Cross-border comparison** - "Stay vs move" analysis
- [ ] **PDF report generation** - Professional output
- [ ] **MCP server** - Expose calculator to AI assistants

**Technical requirements:**
- Structured tax rule database (per jurisdiction)
- PDF generation service
- MCP protocol implementation

### Phase 5: Platform & Scale

**Goals:** Expand reach, enable ecosystem

- [ ] **API marketplace** - Let developers build on our engine
- [ ] **White-label option** - For financial advisors
- [ ] **Advisor dashboard** - Help advisors serve clients
- [ ] **Anonymous benchmarking** - "How do I compare to others like me?"
- [ ] **Community features** - Shared scenarios (opt-in), templates
- [ ] **Additional country modules** - Expand based on demand
- [ ] **Currency handling** - Multi-currency goal tracking

---

## Country Module Specifications

Each tax module should include:

### Data Structure
```
country_module:
  jurisdiction: "US"
  last_updated: "2024-01-15"

  account_types:
    - name: "401(k)"
      contribution_limit: 23000  # 2024
      catch_up_limit: 7500       # age 50+
      tax_treatment: "pre-tax"   # or "post-tax", "tax-free"
      withdrawal_rules:
        - age_59_5: "penalty-free"
        - early: "10% penalty + income tax"
      rmd_required: true
      rmd_start_age: 73
      portability: "rollover to IRA"

  tax_rates:
    capital_gains:
      short_term: "ordinary income"
      long_term:
        - bracket: 0-44625
          rate: 0
        - bracket: 44626-492300
          rate: 0.15
        - bracket: 492301+
          rate: 0.20
    dividends:
      qualified: "same as LTCG"
      ordinary: "ordinary income"

  special_considerations:
    - "NIIT: 3.8% on investment income above $200k single / $250k married"
    - "State taxes vary significantly"
```

### Implementation Approach

**Phase 1:** Hardcoded modules for top 5 countries
**Phase 2:** Structured JSON/YAML database
**Phase 3:** Admin interface for updates
**Phase 4:** Community contributions with review process

### Accuracy & Liability

- All tax information includes "last updated" date
- Clear disclaimers: "For educational purposes only"
- Encourage professional verification
- Annual review process for each module
- User feedback mechanism for corrections

---

## Competitive Positioning

| Feature | Us | ProjectionLab | cFIREsim | Wealthfront |
|---------|----|----|----|----|
| **International focus** | ✅ Core | ❌ US only | ❌ US only | ❌ US only |
| **Tax modules** | ✅ Multi-country | ✅ US only | ❌ | ✅ US only |
| **Privacy-first** | ✅ Local-first | ⚠️ Account required | ✅ | ❌ Needs data |
| **LLM integration** | ✅ Framework + MCP | ❌ | ❌ | ❌ |
| **Free tier** | ✅ Fully functional | ⚠️ Limited | ✅ | ✅ Leads to AUM |
| **Offline capable** | ✅ | ❌ | ✅ | ❌ |
| **Open methodology** | ✅ | ⚠️ | ✅ | ❌ |

**Our unique angle:** International/expat-focused, privacy-preserving, LLM-integrated, independent (no products to sell).

---

## Success Metrics

### Free Tier
- Monthly active users (MAU)
- Framework wizard completion rate
- Return user rate (7-day, 30-day)
- Goals analyzed per user

### Conversion
- Free → Pro conversion rate (target: 2-5%)
- Upgrade trigger identification (which feature wall?)
- Time to conversion (days from first use)

### Paid Tiers
- Monthly recurring revenue (MRR)
- Annual recurring revenue (ARR)
- Churn rate (target: <5% monthly)
- Feature usage by tier
- Net Promoter Score (NPS)

### Product Health
- API response times
- Error rates
- Support ticket volume
- Feature request patterns

---

## Risks & Mitigations

### Regulatory Risk
**Risk:** Could be construed as financial advice
**Mitigation:**
- Clear disclaimers on every page
- "Educational tool" positioning
- No specific product recommendations
- Encourage professional verification

### Tax Accuracy Risk
**Risk:** Tax rules change, modules become outdated
**Mitigation:**
- "Last updated" dates on all modules
- Annual review calendar
- User feedback mechanism
- Conservative assumptions when uncertain

### Competition Risk
**Risk:** Larger player copies our features
**Mitigation:**
- Stay focused on international niche
- Build community/trust (they can't copy that)
- Open source core? (controversial, discuss)
- Move fast on country modules

### Technical Risk
**Risk:** Complexity creep, hard to maintain
**Mitigation:**
- Modular architecture
- Feature flags for staged rollout
- Keep free tier simple
- Automated testing for calculations

---

## Open Questions

1. **Pricing validation** - Is $49/$149 right? Need user research.
2. **Country prioritization** - Which 5 countries first? Based on user demand.
3. **Open source core?** - Pros: trust, community. Cons: harder to monetize.
4. **Advisor channel** - Partner with financial advisors for premium tier?
5. **Mobile app** - PWA sufficient or native apps needed?
6. **Localization** - Translate UI or English-only for now?

---

## Next Steps

1. **Phase 2 planning** - Break down enhanced free tier into tickets
2. **User research** - Interview 10-20 target users on pain points
3. **Pricing validation** - Survey on willingness to pay
4. **Country prioritization** - Poll users on which tax modules matter most
5. **Technical architecture** - Design auth + storage for Pro tier
