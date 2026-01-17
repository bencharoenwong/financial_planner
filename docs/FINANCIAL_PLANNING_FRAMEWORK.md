# Financial Planning Framework

A practical, fill-in-the-blank framework for building your financial plan. Works with any country—you provide the context, an LLM does the research.

**How to use this document:**
1. Fill in Part 1 (your situation)
2. Copy the prompts from Part 2 into Claude/ChatGPT for country-specific research
3. Use our calculator tool to test your numbers (Part 3)
4. Assemble your plan using the template in Part 4
5. Validate with the evaluation prompt in Part 5

**Privacy:** You only share categories and ranges, never exact figures or personal details.

---

## Part 1: Your Situation (Fill This In)

Copy this section and fill in the blanks. You'll paste this into research prompts later.

```
MY SITUATION
============

Location & Status
-----------------
Current tax residency: _______________ (e.g., France, Singapore, USA)
Citizenship(s): _______________ (e.g., Indian citizen, US/UK dual)
Visa status (if applicable): _______________ (e.g., H-1B, work permit, N/A)
Expected location in 5 years: _______________ (same / different country / uncertain)

Age & Career
------------
Age bracket: _______________ (e.g., 25-30, 30-35, 35-40)
Career stage: _______________ (early career / mid-career / senior)
Employment type: _______________ (employee / self-employed / business owner)
Income relative to local median: _______________ (around median / 2-3x / 5x+)

Employer Benefits (if employed)
-------------------------------
Employer retirement scheme: _______________ (yes with match / yes no match / none / unsure)
Match rate (if applicable): _______________%

Financial Foundation
--------------------
Emergency fund: _______________ (none / 1-3 months / 3-6 months / 6+ months)
High-interest debt (>7%): _______________ (none / some / significant)
Current savings rate: _______________% of gross income

Goals
-----
Goal 1: _______________
  - Target amount: _______________
  - Timeline: _______________ years
  - Priority: _______________ (must-have / nice-to-have)

Goal 2: _______________
  - Target amount: _______________
  - Timeline: _______________ years
  - Priority: _______________

Goal 3 (if any): _______________
  - Target amount: _______________
  - Timeline: _______________ years
  - Priority: _______________

Uncertainty Factors
-------------------
Geographic mobility: _______________ (staying put / may relocate / likely moving / highly uncertain)
Career stability: _______________ (stable / moderate variability / high uncertainty)
Major upcoming expenses: _______________ (none / yes: _______________)
```

---

## Part 2: Research Prompts (Copy-Paste Into LLM)

After filling in Part 1, use these prompts to research your specific situation.

### Prompt 2A: Understand Your Country's Options

Copy this entire block, paste into Claude/ChatGPT, and replace the [BRACKETS] with your info from Part 1:

```
I need to understand the tax-advantaged savings options available to me.

MY SITUATION:
- Tax residency: [YOUR TAX RESIDENCY]
- Citizenship: [YOUR CITIZENSHIP]
- Visa status: [YOUR VISA STATUS OR "N/A"]
- Employment type: [EMPLOYEE / SELF-EMPLOYED / ETC]
- Income level: [YOUR INCOME RELATIVE TO MEDIAN]

Please explain:

1. RETIREMENT ACCOUNTS
   - What tax-advantaged retirement accounts exist in [YOUR COUNTRY]?
   - For each account type:
     - Contribution limits (annual)
     - Tax treatment (deductible now? taxed on withdrawal?)
     - Withdrawal rules and penalties
     - What happens if I leave the country?

2. OTHER TAX-ADVANTAGED VEHICLES
   - Investment accounts with special tax treatment
   - Health savings vehicles (if any)
   - Education savings vehicles (if any)

3. EMPLOYER SCHEMES
   - What employer retirement matching is typical in [YOUR COUNTRY]?
   - Vesting schedules
   - Portability if I change jobs

4. INVESTMENT TAXATION
   - How are capital gains taxed? (rate, holding period benefits)
   - How are dividends taxed?
   - Any wealth taxes I should know about?

5. STATE/SOCIAL PENSION
   - What is the public pension system?
   - Contribution requirements
   - Expected benefit level
   - Can I claim if I leave the country?

Please be specific to [YOUR COUNTRY]. If my visa status affects any of these, note that.
```

### Prompt 2B: Portability Analysis (If You May Relocate)

Use this if your mobility level is anything other than "staying put":

```
I may relocate internationally and need to understand how portable different savings vehicles are.

MY SITUATION:
- Current tax residency: [YOUR CURRENT COUNTRY]
- Citizenship: [YOUR CITIZENSHIP]
- Likely destination(s): [WHERE YOU MIGHT MOVE, OR "UNCERTAIN"]
- Timeline: [WHEN YOU MIGHT MOVE]

For each of these account types in [YOUR CURRENT COUNTRY]:
[LIST THE ACCOUNTS FROM PROMPT 2A RESULTS]

Please explain:
1. What happens to this account if I move to [DESTINATION]?
2. Can I continue contributing from abroad?
3. How will withdrawals be taxed? (both countries)
4. Is there a tax treaty that affects this?
5. Should I consider keeping money in taxable/portable accounts instead?

Given my uncertainty level, what allocation between tax-advantaged (but locked) vs taxable (but portable) would you suggest?
```

### Prompt 2C: Specific Scenario Analysis

Use this for specific questions that arise:

```
I have a specific question about my financial planning situation.

MY SITUATION:
[PASTE YOUR FILLED-IN "MY SITUATION" FROM PART 1]

MY QUESTION:
[YOUR SPECIFIC QUESTION - e.g., "Should I max out my CPF top-up or invest in a taxable brokerage given I might return to India in 5 years?"]

Please provide:
1. Direct answer to my question
2. Key factors I should consider
3. What I might be missing
4. Suggested next steps
```

---

## Part 3: Use the Calculator Tool

Now use our Monte Carlo calculator to test your numbers. Here's how the tool outputs map to your plan.

### What to Input

For each goal, enter:

| Field | What to Enter | Where to Get It |
|-------|---------------|-----------------|
| Current Savings | Amount already saved for THIS goal | Your records |
| Target Amount | Goal amount (use "today's buying power") | Part 1 |
| Years | Timeline from Part 1 | Part 1 |
| Monthly Contribution | What you plan to contribute to THIS goal | Your budget |
| Risk Profile | Based on timeline (see below) | Timeline-based |

**Risk Profile Selection:**
- **Conservative**: Timeline < 5 years, or you cannot tolerate volatility
- **Moderate**: Timeline 5-15 years, some flexibility
- **Aggressive**: Timeline 15+ years, won't touch the money

### What the Outputs Mean

| Output | What It Tells You | How to Use It |
|--------|-------------------|---------------|
| **Success Probability** | Likelihood of reaching your goal | Green (80%+) = solid plan. Yellow (50-79%) = stretch. Red (<50%) = needs adjustment |
| **Required Return** | The return needed if using simple compound growth | Compare to risk profile's expected return. If required > expected, plan is aggressive |
| **Percentile Outcomes** | Range of possible ending values | 10th percentile = bad luck scenario. Check if even this is acceptable |

### Record Your Results

Fill this in after running the calculator for each goal:

```
CALCULATOR RESULTS
==================

Goal 1: _______________
  - Inputs: $_______ current, $_______ target, _____ years, $_______ /month, _______ risk
  - Success Probability: _______%  [GREEN / YELLOW / RED]
  - Required Return: _______%
  - 10th Percentile Outcome: $_______
  - Assessment: [ON TRACK / STRETCH / NEEDS WORK]

Goal 2: _______________
  - Inputs: $_______ current, $_______ target, _____ years, $_______ /month, _______ risk
  - Success Probability: _______%  [GREEN / YELLOW / RED]
  - Required Return: _______%
  - 10th Percentile Outcome: $_______
  - Assessment: [ON TRACK / STRETCH / NEEDS WORK]

Goal 3: _______________
  - Inputs: $_______ current, $_______ target, _____ years, $_______ /month, _______ risk
  - Success Probability: _______%  [GREEN / YELLOW / RED]
  - Required Return: _______%
  - 10th Percentile Outcome: $_______
  - Assessment: [ON TRACK / STRETCH / NEEDS WORK]

TOTAL MONTHLY CONTRIBUTION ACROSS ALL GOALS: $_______
```

### If Results Are Yellow or Red

Adjust one or more of:
- **Increase contribution** → Re-run calculator
- **Extend timeline** → Re-run calculator
- **Reduce target** → Re-run calculator
- **Accept more risk** → Only if timeline supports it

Re-run until you have a plan you're comfortable with.

---

## Part 4: Assemble Your Plan

Now combine everything into your actual plan.

### Your Financial Plan Template

```
MY FINANCIAL PLAN
=================
Created: [DATE]
Review by: [DATE + 3-6 MONTHS]

SITUATION SUMMARY
-----------------
[Paste your filled-in "MY SITUATION" from Part 1]

RESEARCH FINDINGS
-----------------
Tax-advantaged accounts I'll use:
1. [ACCOUNT TYPE]: [WHY - from Prompt 2A results]
2. [ACCOUNT TYPE]: [WHY]

Accounts I'm NOT using and why:
- [ACCOUNT]: [REASON - e.g., "not portable, and I may relocate"]

Key tax considerations:
- [FINDING 1 from research]
- [FINDING 2]

GOALS & ALLOCATION
------------------
Monthly savings budget: $_______ (____% of gross income)

Goal 1: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Strategy: $_______ /month into [ACCOUNT TYPE]
  Risk profile: [CONSERVATIVE/MODERATE/AGGRESSIVE]
  Calculator probability: _______%

Goal 2: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Strategy: $_______ /month into [ACCOUNT TYPE]
  Risk profile: [CONSERVATIVE/MODERATE/AGGRESSIVE]
  Calculator probability: _______%

Goal 3: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Strategy: $_______ /month into [ACCOUNT TYPE]
  Risk profile: [CONSERVATIVE/MODERATE/AGGRESSIVE]
  Calculator probability: _______%

ALLOCATION SUMMARY
------------------
Total monthly: $_______

By account type:
- [ACCOUNT 1]: $_______ /month (Goal: _______)
- [ACCOUNT 2]: $_______ /month (Goal: _______)
- Taxable brokerage: $_______ /month (Goal: _______)

EMPLOYER BENEFITS CHECKLIST
---------------------------
[ ] Contributing enough to get full employer match
[ ] Understand vesting schedule
[ ] Know what happens if I leave

FOUNDATION CHECKLIST
--------------------
[ ] Emergency fund: _____ months (target: 3-6)
[ ] High-interest debt: [PAID OFF / IN PROGRESS / N/A]

UNCERTAINTIES & CONTINGENCIES
-----------------------------
If I relocate to [COUNTRY]:
- [WHAT CHANGES - from Prompt 2B]

If income changes significantly:
- [ADJUSTMENT PLAN]

REVIEW TRIGGERS
---------------
Re-run calculator and update this plan when:
- [ ] Major life change (job, marriage, kids, relocation)
- [ ] Income changes >20%
- [ ] Every 6-12 months regardless
- [ ] Market drops >30% (check if still on track)

OPEN QUESTIONS
--------------
- [QUESTION 1 - for future research]
- [QUESTION 2]
```

---

## Part 5: Evaluate Your Plan

Before finalizing, use this prompt to check your plan:

```
Please evaluate my financial plan for internal consistency and obvious gaps.
Do NOT give me a new plan—just identify issues with MY plan.

MY SITUATION:
[PASTE YOUR "MY SITUATION" FROM PART 1]

MY RESEARCH FINDINGS:
[PASTE KEY FINDINGS FROM PROMPTS 2A/2B]

MY PLAN:
[PASTE YOUR COMPLETED PLAN FROM PART 4]

CALCULATOR RESULTS:
[PASTE YOUR CALCULATOR RESULTS FROM PART 3]

Please check:

1. MATH CHECK
   - Do my monthly contributions add up correctly?
   - Is my total savings rate reasonable for my income level?
   - Do the calculator probabilities support my goals?

2. ACCOUNT CHOICE CHECK
   - Am I using the right accounts for each goal given my situation?
   - Am I leaving tax benefits on the table?
   - Does my portability allocation match my mobility level?

3. PRIORITY CHECK
   - Am I funding goals in the right order?
   - Is anything missing (emergency fund, debt, employer match)?

4. CONSISTENCY CHECK
   - Do my stated uncertainties match my account choices?
   - Are my risk profiles appropriate for my timelines?

5. GAPS
   - What am I not thinking about?
   - What questions should I research further?

Be direct. If something doesn't make sense, say so.
```

---

## Quick Reference: The Full Workflow

```
┌─────────────────────────────────────────────────────────┐
│ 1. FILL IN YOUR SITUATION (Part 1)                      │
│    → Country, goals, constraints, uncertainties         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 2. RESEARCH YOUR OPTIONS (Part 2)                       │
│    → Copy prompts into Claude/ChatGPT                   │
│    → Learn your country's tax-advantaged accounts       │
│    → Understand portability if you may relocate         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 3. TEST YOUR NUMBERS (Part 3)                           │
│    → Use the Monte Carlo calculator for each goal       │
│    → Record probability, required return, percentiles   │
│    → Adjust until GREEN or acceptable YELLOW            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 4. ASSEMBLE YOUR PLAN (Part 4)                          │
│    → Combine situation + research + calculator results  │
│    → Specify account types for each goal                │
│    → Document contingencies and review triggers         │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 5. VALIDATE (Part 5)                                    │
│    → Use evaluation prompt to check for gaps            │
│    → Address any issues found                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 6. EXECUTE & REVIEW                                     │
│    → Set up automatic contributions                     │
│    → Review quarterly or when life changes              │
│    → Re-run calculator annually                         │
└─────────────────────────────────────────────────────────┘
```

---

## Notes

**What this framework does:**
- Gives you fillable templates to structure your thinking
- Provides ready-to-use prompts for LLM research
- Shows exactly how calculator outputs fit into your plan
- Helps you validate your plan for consistency

**What this framework does NOT do:**
- Provide specific investment advice
- Replace professional tax/legal advice for complex situations
- Guarantee any outcomes

**When to get professional help:**
- Cross-border tax situations with significant assets
- Business ownership with complex equity
- Estate planning
- If you're unsure about anything significant
