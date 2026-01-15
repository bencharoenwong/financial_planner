# Product Requirements Document: Gamified Financial Planner

**Version:** 1.0
**Date:** 2026-01-14
**Status:** Draft

---

## 1. Problem Statement

### The Onboarding Paradox in Financial Planning

Financial planning tools face a fundamental tension:

| Approach | Problem |
|----------|---------|
| **Deep upfront questionnaire** | User fatigue, abandonment rates 60-80%, feels like a tax form |
| **Minimal questions** | Generic advice ("save more, spend less"), users don't feel understood |

This creates a lose-lose: users either quit before getting value, or they receive advice so generic it's useless.

### Why This Matters

- **Trust gap:** Users don't trust a system that doesn't know them
- **Engagement cliff:** Front-loaded complexity kills retention before habit formation
- **Personalization debt:** Systems that skip onboarding never catch up on personalization

### The Duolingo Insight

Duolingo solved an analogous problem in language learning:
- Traditional approach: Placement test → curriculum → grind
- Duolingo approach: Start immediately → learn preferences through play → adapt continuously

**Key principle:** Replace interrogation with interaction. Learn about users *while* they're getting value, not before.

---

## 2. Product Vision

### One-Liner
A financial planning experience that learns what you need by watching what you do, not by asking what you want.

### Core Philosophy

1. **Value-first, questions later:** User should feel they're getting something useful within 60 seconds
2. **Progressive disclosure:** Collect information in small doses, tied to immediate benefit
3. **Implicit > Explicit:** Infer from behavior when possible; ask only when necessary
4. **Gamification as feedback loop:** Points/streaks aren't gimmicks—they're the mechanism for sustained engagement that enables deeper personalization over time

---

## 3. Target Users

### Primary Persona: "Anxious Avoider"
- **Demographics:** 25-45, income $50K-$150K
- **Behavior:** Knows they *should* plan, feels overwhelmed, has started and abandoned 2-3 tools
- **Pain:** "Every app asks me 50 questions then tells me to save more. I already know that."
- **Goal:** Feel in control without becoming a spreadsheet person

### Secondary Persona: "Curious Optimizer"
- **Demographics:** 28-40, income $80K-$200K
- **Behavior:** Already tracks spending, wants more sophisticated planning
- **Pain:** "Mint tells me I spent $400 on food. So what? What should I actually do?"
- **Goal:** Actionable insights, not just dashboards

### Anti-Persona: "DIY Spreadsheet Expert"
- Already has custom systems, wants raw data export
- Not our target—they'll churn regardless of gamification

---

## 4. Onboarding Design: The Duolingo Model Applied

### Phase 0: Zero-Question Start (0-60 seconds)

**Duolingo equivalent:** "I want to learn Spanish" → immediately start a lesson

**Our version:**
```
[Single screen]
"What's on your mind today?"

[ ] I'm worried about money
[ ] I want to save for something specific
[ ] I'm curious where my money goes
[ ] Just exploring

→ [Let's go]
```

No account creation required. No income questions. No net worth calculator.

**Why this works:**
- Self-selection reveals intent without interrogation
- Each path leads to an immediately useful micro-experience
- Account creation happens *after* the user gets value

### Phase 1: First Value Moment (1-5 minutes)

Based on selection, deliver a focused micro-experience:

| Selection | Immediate Experience |
|-----------|---------------------|
| "Worried about money" | 3-question stress assessment → personalized "one thing to do today" |
| "Save for something" | Goal visualizer → "you need $X/month" → savings game |
| "Where my money goes" | Quick category sort game → insight reveal |
| "Just exploring" | Financial personality quiz → archetype reveal |

**Critical:** Each path teaches us something while delivering value.

### Phase 2: Progressive Profiling (Days 1-14)

Instead of one 50-question survey, we ask 1-2 questions per session, always tied to immediate utility:

| Session | Question | Tied To |
|---------|----------|---------|
| 2 | "Roughly what do you earn?" (slider, not exact) | Unlocks budget suggestions |
| 3 | "Do you have an emergency fund?" (Y/N) | Unlocks savings priority |
| 5 | "Any debt bothering you?" | Unlocks debt payoff game |
| 7 | "What's your living situation?" | Unlocks housing module |

**The trade:** Each question unlocks a new feature or insight. Users see the value exchange.

### Phase 3: Behavioral Inference (Ongoing)

After account linking (optional, incentivized):

| Behavior | Inference | No Question Needed |
|----------|-----------|-------------------|
| Netflix + Spotify + gym charges | Subscription conscious | Recommend subscription audit game |
| Friday night restaurant spikes | Social spender | Don't shame; offer "fun money" budget |
| Consistent savings transfers | Already disciplined | Skip basic savings advice |
| Overdraft fees | Cash flow timing issue | Offer bill timing optimizer |

---

## 5. Gamification Framework

### Core Loop: Daily Financial "Workout"

**Duration:** 2-3 minutes
**Frequency:** Daily (with streak incentives)

```
┌─────────────────────────────────────────┐
│         TODAY'S FINANCIAL WORKOUT       │
├─────────────────────────────────────────┤
│                                         │
│  🎯 Quick Challenge (30 sec)            │
│     "Guess your food spending this week"│
│     [Your guess: $___]                  │
│                                         │
│  📊 One Insight                         │
│     "You spent 23% less on transport    │
│      than last month. Nice."            │
│                                         │
│  ✅ One Action                          │
│     "Move $50 to savings?"              │
│     [Yes] [Not today]                   │
│                                         │
│  🔥 Streak: 7 days                      │
│                                         │
└─────────────────────────────────────────┘
```

### Progression System

| Level | Name | Unlocks |
|-------|------|---------|
| 1-5 | **Starter** | Basic tracking, daily insights |
| 6-10 | **Saver** | Goal setting, savings games |
| 11-15 | **Strategist** | Debt optimization, what-if scenarios |
| 16-20 | **Planner** | Long-term projections, retirement preview |
| 21+ | **Master** | Advanced analytics, community features |

**XP Sources:**
- Daily check-in: 10 XP
- Completing a challenge: 20-50 XP
- Hitting a savings goal: 100 XP
- Learning module completion: 50 XP
- Streak bonus: 5 XP × streak days

### Engagement Mechanics (Borrowed from Duolingo)

| Mechanic | Financial Application |
|----------|----------------------|
| **Streak** | Consecutive days of engagement; "freeze" option |
| **Hearts/Lives** | Budget "lives" lost when overspending category |
| **Leaderboards** | Anonymous savings rate competition (opt-in) |
| **Achievements** | "First $1K saved," "Debt-free month," etc. |
| **Stories** | Narrative scenarios: "Help Alex decide: vacation or investing?" |

### Anti-Shame Design

**Critical principle:** Never make users feel bad about their finances.

| Instead of... | We say... |
|---------------|-----------|
| "You overspent by $200" | "Busy month! Here's what you prioritized:" |
| "You're behind on savings" | "Want to do a savings sprint this week?" |
| "Your debt is high" | "Let's play the debt snowball game" |

---

## 6. Core Features (MVP)

### 6.1 The Daily Workout
- 2-3 minute daily engagement
- Personalized based on user's current focus
- Always ends with one clear action

### 6.2 Goal Games
- Visual savings progress (jar filling, mountain climbing, etc.)
- Micro-goals: "Save $20 this week" not "Save $10,000 this year"
- Celebration animations on milestones

### 6.3 Money Personality System
- Archetype assignment (Saver, Spender, Avoider, etc.)
- Personalized advice based on archetype
- "Your type tends to... so try..."

### 6.4 Challenge Mode
- Weekly spending challenges: "No-spend weekend"
- Competitive mode: Beat your past self
- Social mode: Challenge a friend (anonymous amounts)

### 6.5 Learning Bites
- 60-second financial concepts
- Quiz format with XP rewards
- Unlocked progressively based on relevance

### 6.6 Smart Notifications
- Streak reminders (non-annoying)
- "You're close to a goal" nudges
- Bill payment heads-up
- Positive reinforcement ("3rd week under budget!")

---

## 7. Information Architecture

### What We Learn vs. When We Learn It

| Information | How Acquired | When |
|-------------|--------------|------|
| Financial stress level | Opening question | Minute 1 |
| Primary goal | Opening question | Minute 1 |
| Rough income | Asked (with unlock) | Day 2-3 |
| Spending patterns | Bank link or manual | Day 3-7 |
| Debt situation | Asked (with unlock) | Day 5-10 |
| Risk tolerance | Inferred from choices | Ongoing |
| Life stage | Inferred + asked | Week 2 |
| Exact net worth | Optional deep dive | When user chooses |

### The "Never Ask" List

Things we infer rather than ask:
- Exact income (use ranges)
- Exact net worth (calculate from linked accounts if available)
- Risk tolerance (observe choices in scenarios)
- Spending guilt (observe engagement patterns)

---

## 8. Technical Considerations

### Data Requirements

| Data Type | Source | Required? |
|-----------|--------|-----------|
| Transaction data | Plaid/MX/manual | Optional (but incentivized) |
| User responses | In-app | Yes |
| Behavioral signals | Analytics | Yes |
| Goal progress | Calculated | Yes |

### Personalization Engine

```
User State = {
    explicit_profile,      // What they told us
    inferred_profile,      // What we learned from behavior
    engagement_history,    // Streaks, XP, completions
    current_goals,         // Active savings/debt goals
    last_insight_shown,    // Avoid repetition
    preferred_difficulty   // Adapts challenge level
}

Daily_Content = f(User_State, Day_of_Week, Season, Market_Conditions)
```

### Privacy-First Design

- Aggregated insights by default
- Exact transaction details require explicit opt-in
- No selling of data
- Clear value exchange for each data request

---

## 9. Success Metrics

### North Star Metric
**Weekly Active Users who complete Daily Workout 4+ days/week**

### Funnel Metrics

| Stage | Metric | Target |
|-------|--------|--------|
| Acquisition | First session completion | >80% |
| Activation | Return for Day 2 | >50% |
| Engagement | 7-day retention | >40% |
| Monetization | Premium conversion (if applicable) | >5% |
| Referral | Users who invite friends | >10% |

### Engagement Metrics

- Average streak length
- Daily Workout completion rate
- Questions answered per session (should be low, 1-2)
- XP earned per week
- Goals created and achieved

### Anti-Metrics (What We Don't Optimize)

- Time in app (not a goal—efficient > sticky)
- Questions asked (fewer is better)
- Notifications sent (quality > quantity)

---

## 10. Competitive Landscape

| Competitor | Approach | Gap We Fill |
|------------|----------|-------------|
| **Mint** | Dashboard-first, passive tracking | No action guidance, no engagement loop |
| **YNAB** | Budget-first, manual entry | High learning curve, time-intensive |
| **Copilot** | AI chat, premium | Expensive, still front-loads questions |
| **Cleo** | Chatbot, personality | Fun but shallow, limited planning |
| **Betterment/Wealthfront** | Investment-focused | Ignores daily finances |

**Our positioning:** The only financial tool designed for people who've quit other financial tools.

---

## 11. Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Gamification feels patronizing | Tone matters: respect, not cheerleading. Test extensively. |
| Users game the system for XP | XP tied to real actions (savings transfers, not just opens) |
| Insufficient personalization from limited data | Behavioral inference engine; transparent "unlock more" prompts |
| Streak pressure creates anxiety | Streak freezes; "life happens" mode; no harsh penalties |
| Privacy concerns with bank linking | Bank link optional; app valuable without it |

---

## 12. Open Questions for Further Research

1. **Monetization model:** Freemium? Subscription? B2B (employers/banks)?
2. **Advisor integration:** Does a human advisor ever enter the loop?
3. **Investment extension:** How far does this go beyond budgeting?
4. **Household mode:** Joint finances, different archetypes?
5. **International:** Currency/banking system variations?

---

## 13. Appendix: Duolingo Mechanics Deep Dive

### What Duolingo Gets Right

1. **Immediate value:** First lesson in <60 seconds, no signup required
2. **Microlearning:** 5-minute sessions, not 30-minute commitments
3. **Progressive difficulty:** Adapts to demonstrated skill
4. **Spaced repetition:** Revisits concepts at optimal intervals
5. **Social proof:** "1M people learning Spanish today"
6. **Loss aversion:** Streaks create commitment
7. **Variable rewards:** Different challenges, surprise bonuses

### Translation to Finance

| Duolingo | Financial Planner |
|----------|-------------------|
| Learn vocabulary | Learn spending patterns |
| Practice pronunciation | Practice budgeting |
| Placement test | Financial stress assessment |
| Lesson streaks | Engagement streaks |
| Language fluency | "Financial fitness" score |
| Stories | Financial scenarios |
| Leaderboards | Savings rate competition |

---

## 14. Next Steps

1. **User research:** Interview 20 "anxious avoiders" about past tool failures
2. **Prototype:** Build first-value-moment flows for each entry path
3. **Tone testing:** A/B test gamification language (fun vs. serious)
4. **Technical spike:** Evaluate transaction categorization accuracy
5. **Competitive audit:** Deep dive on Cleo, Copilot engagement mechanics

---

*This PRD is a living document. Update as research and prototyping reveal new insights.*
