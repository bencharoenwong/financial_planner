# Product Direction: Decision Summary

> Two different product visions exist. This doc clarifies the choice.

---

## The Fork in the Road

We have two very different product concepts documented:

### Option A: "Goal Calculator" (PRD.md)

**What it is:** Lightweight Monte Carlo calculator for financial goal feasibility

**Core interaction:** Input numbers → Get probability → Done (or save locally)

**Engagement model:** Calm, quarterly. "Check back when your numbers change."

**Data requirements:** None stored. User self-reports. No bank linking.

**Build complexity:** Low. Current codebase is 90% complete.

**Target user:** Someone asking "Can I retire with $X?"

### Option B: "Gamified Financial Coach" (PRD_GAMIFICATION.md)

**What it is:** Daily engagement app with Duolingo-style mechanics

**Core interaction:** 2-3 minute daily "workout" with challenges, streaks, XP

**Engagement model:** Daily. Habit formation through gamification.

**Data requirements:** Bank account linking (Plaid), transaction categorization, behavioral inference engine

**Build complexity:** High. Requires user accounts, database, Plaid integration, personalization engine, notification system.

**Target user:** Someone who's quit Mint/YNAB and wants something "fun"

---

## Comparison Table

| Dimension | Option A: Calculator | Option B: Gamified |
|-----------|---------------------|-------------------|
| **Time to useful v1** | Weeks | Months |
| **Infrastructure** | Static site + API | Full stack + Plaid + DB |
| **User accounts** | Not required | Required |
| **Ongoing cost** | Near zero | Plaid fees, hosting, DB |
| **Regulatory risk** | Minimal (calculator) | Higher (handles bank data) |
| **Differentiation** | "Transparent math, no sales pitch" | "Finally, a finance app that's fun" |
| **Market** | Underserved (simple tools are rare) | Crowded (Cleo, Copilot, etc.) |
| **Monetization** | API licensing, B2B, brand | Freemium, B2C subscriptions |

---

## The Honest Assessment

### Arguments FOR Option A (Calculator)

1. **Already built.** Current code works. Ship it.
2. **Clear value prop.** "Am I on track?" is a question everyone has.
3. **No competitive moat needed.** Simplicity IS the moat.
4. **Zero ongoing cost.** Vercel free tier, no database, no Plaid.
5. **No regulatory complexity.** It's a calculator, not a financial service.
6. **B2B potential.** Financial advisors want this. API licensing is real.

### Arguments FOR Option B (Gamified)

1. **Bigger market.** B2C scale is larger than B2B.
2. **Retention.** Daily engagement creates defensible user relationships.
3. **Data moat.** User behavior data enables better personalization.
4. **Brand building.** Consumer apps create brand awareness.
5. **Duolingo proved it works.** Gamification can make boring things engaging.

### Arguments AGAINST Option B (Gamified)

1. **Crowded market.** Cleo, Copilot, Rocket Money, Monarch all exist.
2. **Expensive to build.** Plaid = $0.20-$2.00 per user per month.
3. **Finance ≠ Language.** Daily engagement may be counterproductive (see COMPETITIVE_ANALYSIS.md).
4. **Regulatory surface.** Bank data = compliance burden.
5. **Gamification fatigue.** Users are getting tired of "everything is Duolingo."

---

## Recommendation

**Start with Option A. Validate the core value prop before adding complexity.**

### Rationale

1. **Option A is a prerequisite for Option B.** The Monte Carlo engine is needed either way. Ship it, get users, learn.

2. **Option B assumptions are untested.** We're guessing that gamification works for finance. Duolingo comparisons are appealing but potentially misleading.

3. **Resource efficiency.** Option A can ship this month. Option B is a multi-quarter project.

4. **Reversibility.** A→B is easy (add features). B→A is hard (can't simplify a complex app).

### Proposed Path

```
Now        → Ship Option A (calculator)
Month 2    → Add local storage scenarios
Month 3-4  → Monitor usage, interview users
Month 5+   → IF validation succeeds, THEN consider gamification layer
```

---

## Questions for Decision Makers

1. **What's the business goal?**
   - Brand building for Chicago Global? → Option A is sufficient
   - Consumer product line? → Option B may be worth the investment

2. **What's the timeline pressure?**
   - Need something live soon? → Option A
   - Building for 18-month horizon? → Option B might make sense

3. **What's the appetite for operational complexity?**
   - Prefer minimal ongoing costs? → Option A
   - Willing to run infrastructure? → Option B is feasible

4. **Who's the customer?**
   - B2B (advisors, fintechs)? → Option A is the product
   - B2C (retail users)? → Option B might be necessary for scale

---

## Files Reference

| Document | Contents |
|----------|----------|
| `PRD.md` | Option A: Calculator-focused product |
| `PRD_GAMIFICATION.md` | Option B: Duolingo-style engagement |
| `COMPETITIVE_ANALYSIS.md` | Why gamification may not transfer to finance |
| `DATA_ARCHITECTURE.md` | Privacy-first design (supports Option A) |

---

*Decision needed: Which direction?*
