# Financial Planning Framework

A professional framework for comprehensive financial planning. Works for any jurisdiction—you provide the context, an LLM provides jurisdiction-specific research.

**How to use this document:**
1. Complete your situation profile (Part 1)
2. Use the appropriate prompts from Part 2 for your complexity level
3. Test your numbers with our calculator (Part 3)
4. Assemble your plan (Part 4)
5. Validate with the review prompt (Part 5)

**Privacy by design:** Share only categories and ranges, never exact figures or identifying details.

**Important:** This framework facilitates research and planning. It does not constitute financial, tax, or legal advice. Consult qualified professionals for significant decisions.

---

## Part 1: Your Situation Profile

Complete this profile before using any prompts. The level of detail determines which prompts are relevant.

```
SITUATION PROFILE
=================

SECTION A: RESIDENCY & CITIZENSHIP
----------------------------------
Current tax residency: _______________
Citizenship(s): _______________ (note if dual/multiple)
Visa/immigration status: _______________ (permanent resident, work visa type, citizen, etc.)
Years in current residence: _______________
Expected location in 5 years: _______________ (same / different country / uncertain)
Prior residencies (last 10 years): _______________

SECTION B: CAREER & INCOME
--------------------------
Age bracket: _______________ (25-30 / 30-35 / 35-40 / 40-50 / 50-60 / 60+)
Primary role: _______________ (employee / executive / business owner / self-employed / retired)
Industry: _______________ (finance / tech / consulting / healthcare / other: ___)
Income level vs local median: _______________ (1-2x / 2-5x / 5-10x / 10x+)

Income composition (check all that apply):
[ ] Base salary
[ ] Annual bonus (cash)
[ ] Equity compensation (RSUs, stock options, ESPP)
[ ] Carried interest / profit participation
[ ] Partnership/LLC distributions
[ ] Deferred compensation (NQDC plans)
[ ] Board fees / consulting income
[ ] Rental / investment income
[ ] Business distributions / dividends
[ ] Other: _______________

SECTION C: EQUITY COMPENSATION (if applicable)
----------------------------------------------
Types held: _______________ (RSUs / ISOs / NSOs / ESPP / phantom stock / other)
Vesting schedule: _______________ (4-year cliff / graded / performance-based)
Concentrated stock position (>10% of NW): _______________ (yes / no)
Company status: _______________ (public / pre-IPO / private)
10b5-1 plan in place: _______________ (yes / no / N/A)

SECTION D: EMPLOYER BENEFITS
----------------------------
Retirement plan type: _______________ (401k / pension / DC scheme / none / multiple)
Employer match: _______________ (% and cap, if any)
Match vesting: _______________ (immediate / graded over ___ years / cliff at ___ years)
Deferred comp available: _______________ (yes / no)
Executive benefits: _______________ (SERP, split-dollar life, other: ___)
Stock purchase plan: _______________ (ESPP discount: ___%, lookback: yes/no)

SECTION E: BUSINESS INTERESTS (if applicable)
---------------------------------------------
Business structure: _______________ (sole prop / LLC / S-corp / C-corp / partnership)
Ownership %: _______________
Business valuation (approx): _______________
Succession plan: _______________ (in place / in progress / none)
Buy-sell agreement: _______________ (yes / no)
Key person insurance: _______________ (yes / no)

SECTION F: FINANCIAL FOUNDATION
-------------------------------
Emergency fund: _______________ (months of expenses)
High-interest debt (>7%): _______________ (none / some / significant)
Mortgage(s): _______________ (rate: ___%, years remaining: ___)
Current savings rate: _______________% of gross income
Existing retirement accounts: _______________ (types and approximate totals)

SECTION G: GOALS (ranked by priority)
-------------------------------------
Goal 1: _______________
  - Target amount: _______________ (in today's purchasing power)
  - Timeline: _______________ years
  - Flexibility: _______________ (fixed date / flexible / aspirational)

Goal 2: _______________
  - Target amount: _______________
  - Timeline: _______________ years
  - Flexibility: _______________

Goal 3: _______________
  - Target amount: _______________
  - Timeline: _______________ years
  - Flexibility: _______________

SECTION H: RISK FACTORS & CONSTRAINTS
-------------------------------------
Geographic mobility: _______________ (anchored / may relocate / likely moving / highly mobile)
Income stability: _______________ (stable / variable / highly volatile)
Career trajectory: _______________ (growth expected / plateau / winding down)
Health considerations: _______________ (standard / chronic conditions / high-cost expected)
Family obligations: _______________ (dependents, aging parents, education funding, etc.)
Liquidity constraints: _______________ (locked equity, restricted stock, illiquid assets)

SECTION I: EXISTING STRUCTURES
------------------------------
Trusts: _______________ (grantor / non-grantor / foreign / none)
Holding companies: _______________ (yes / no)
Life insurance policies: _______________ (term / whole / VUL / none)
Existing tax elections: _______________ (83(b) filed / QSBS claimed / other)
```

---

## Part 2: Research Prompts

Select prompts based on your situation complexity. Start with 2A (everyone needs this), then add specialized prompts as relevant.

### Prompt 2A: Tax-Advantaged Accounts & Investment Taxation (Core)

Use this for baseline country-specific research:

```
I need to understand the tax-advantaged savings options and investment taxation in my jurisdiction.

MY SITUATION:
- Tax residency: [COUNTRY]
- Citizenship: [CITIZENSHIP(S)]
- Immigration status: [VISA TYPE OR CITIZEN/PR]
- Employment type: [EMPLOYEE / SELF-EMPLOYED / BUSINESS OWNER]
- Income level: [X TIMES LOCAL MEDIAN]

Please provide comprehensive information on:

1. RETIREMENT ACCOUNTS
   For each available account type:
   - Name and structure (e.g., 401(k), ISA, CPF, superannuation)
   - 2024/2025 contribution limits (employee and employer portions)
   - Tax treatment: deductible contributions? tax-deferred growth? taxed on withdrawal?
   - Early withdrawal penalties and exceptions
   - Required minimum distributions (if any)
   - Portability: what happens if I leave this country?
   - Creditor protection status

2. NON-RETIREMENT TAX-ADVANTAGED ACCOUNTS
   - Investment accounts with preferential treatment (ISA, PEA, TFSA, etc.)
   - Health savings vehicles (HSA, etc.)
   - Education savings vehicles (529, RESP, etc.)
   - Any wealth-building incentives (first-home savers, etc.)

3. INVESTMENT TAXATION
   - Capital gains: rates, holding period benefits, indexation
   - Dividends: qualified vs ordinary treatment, foreign dividend treatment
   - Interest income taxation
   - Tax-loss harvesting rules and wash sale restrictions
   - Wealth/net worth taxes (if any)
   - Exit taxes on emigration (if any)

4. SOCIAL SECURITY / STATE PENSION
   - Contribution requirements and rates
   - Expected benefit calculation methodology
   - Vesting requirements for portability
   - Claiming from abroad (totalization agreements)

5. EMPLOYER RETIREMENT SCHEMES
   - Typical employer matching formulas
   - Vesting schedules
   - What happens to unvested amounts if I leave?

Be specific to [COUNTRY]. Note any restrictions based on my immigration status.
```

### Prompt 2B: Cross-Border Portability Analysis

Use this if you may relocate internationally:

```
I need to understand cross-border tax implications for my savings and investments.

MY SITUATION:
- Current tax residency: [CURRENT COUNTRY]
- Citizenship: [CITIZENSHIP(S)]
- Possible future residencies: [DESTINATION(S) OR "UNCERTAIN"]
- Timeline: [WHEN RELOCATION MAY OCCUR]
- Is US citizenship/green card involved? [YES/NO]

ACCOUNTS I HOLD OR AM CONSIDERING:
[LIST SPECIFIC ACCOUNTS FROM PROMPT 2A RESULTS]

For each account type, explain:

1. CONTINUED CONTRIBUTIONS
   - Can I contribute after becoming non-resident?
   - Are contributions still tax-advantaged from abroad?

2. INVESTMENT RESTRICTIONS
   - PFIC issues for US persons investing abroad
   - Mutual fund restrictions for non-residents
   - ETF domicile considerations (US vs Ireland-domiciled)

3. WITHDRAWAL TAXATION
   - How are withdrawals taxed in my origin country?
   - How are withdrawals taxed in my destination country?
   - Applicable tax treaty provisions (withholding rates, treaty benefits)
   - Double taxation relief mechanisms

4. EXIT TAX CONSIDERATIONS
   - Deemed disposition rules on departure
   - Mark-to-market requirements
   - Planning opportunities before exit

5. REPORTING OBLIGATIONS
   - FBAR (FinCEN 114) requirements
   - FATCA Form 8938 requirements
   - CRS reporting implications
   - Foreign trust reporting (Forms 3520/3520-A)
   - Controlled Foreign Corporation rules (Form 5471)

6. TAX TREATY ANALYSIS
   - [ORIGIN]-[DESTINATION] tax treaty provisions
   - Tie-breaker rules for dual residents
   - Pension article treatment
   - Capital gains articles
   - Limitation on benefits clauses

7. OPTIMAL STRUCTURE
   Given my mobility level of [ANCHORED/MAY RELOCATE/HIGHLY MOBILE]:
   - What % should be in portable taxable accounts?
   - What % in tax-advantaged but jurisdiction-locked accounts?
   - Any structures that work well across multiple jurisdictions?
```

### Prompt 2C: Equity Compensation Planning

Use this if you have stock options, RSUs, or other equity awards:

```
I need guidance on tax-efficient management of equity compensation.

MY SITUATION:
- Tax residency: [COUNTRY]
- Citizenship: [CITIZENSHIP(S)]
- Company: [PUBLIC / PRE-IPO / PRIVATE]
- Equity types: [RSUs / ISOs / NSOs / ESPP / OTHER]

EQUITY DETAILS:
- Current unvested value (approx): [RANGE]
- Vesting schedule: [E.G., 4-YEAR WITH 1-YEAR CLIFF]
- Strike price vs current FMV (for options): [UNDERWATER / AT MONEY / IN THE MONEY BY X%]
- Concentrated position (>10% of NW): [YES/NO]
- Trading window restrictions: [YES/NO]
- 10b5-1 plan: [IN PLACE / CONSIDERING / N/A]

Please advise on:

1. TAX TREATMENT BY AWARD TYPE
   - RSU taxation at vesting
   - ISO: AMT implications, qualifying vs disqualifying dispositions
   - NSO: ordinary income at exercise, subsequent capital gains
   - ESPP: holding period requirements, discount taxation

2. TIMING STRATEGIES
   - Exercise timing for options (early exercise, 83(b) elections)
   - RSU delivery timing (if deferral available)
   - ESPP purchase timing and holding optimization
   - Coordination with other income years

3. DIVERSIFICATION STRATEGIES
   - Systematic selling programs (10b5-1 plans)
   - Hedging strategies (collars, prepaid forwards)
   - Exchange funds for concentrated positions
   - Charitable strategies (donor-advised funds, CRTs)

4. CROSS-BORDER COMPLICATIONS
   - Equity compensation across multiple tax years in different countries
   - Sourcing rules for multi-year grants
   - Treaty treatment of equity compensation
   - Social security implications

5. LIQUIDITY EVENTS
   - IPO planning and lockup considerations
   - M&A scenarios (cash vs stock consideration)
   - QSBS eligibility and Section 1202 exclusion
   - Installment sales and structured exits

6. RISK MANAGEMENT
   - Concentration risk assessment
   - Company-specific vs market risk
   - Liquidity needs vs tax optimization trade-offs
```

### Prompt 2D: Business Owner Planning

Use this if you own a business:

```
I need comprehensive planning guidance as a business owner.

MY SITUATION:
- Tax residency: [COUNTRY]
- Business structure: [LLC / S-CORP / C-CORP / PARTNERSHIP / OTHER]
- Industry: [INDUSTRY]
- Revenue range: [RANGE]
- Ownership: [%] (other owners: family / partners / investors)
- Years in business: [NUMBER]

Please advise on:

1. RETIREMENT PLAN OPTIONS
   - SEP-IRA vs SIMPLE IRA vs Solo 401(k) vs defined benefit
   - Contribution limits for each
   - Employee coverage requirements
   - Cash balance plan considerations for high earners

2. ENTITY STRUCTURE OPTIMIZATION
   - S-corp reasonable compensation rules
   - Self-employment tax optimization
   - C-corp accumulation strategies
   - Holding company structures

3. TAX PLANNING STRATEGIES
   - Qualified Business Income (QBI) deduction (Section 199A)
   - Timing of income and deductions
   - Equipment and vehicle deductions (Section 179, bonus depreciation)
   - R&D tax credits
   - State tax planning (entity-level taxes, nexus issues)

4. EXIT PLANNING
   - QSBS (Qualified Small Business Stock) eligibility and planning
   - Installment sales
   - Opportunity Zone deferrals
   - ESOP transactions
   - Strategic vs financial buyer implications
   - Earnout structuring

5. SUCCESSION PLANNING
   - Buy-sell agreement funding and structure
   - Valuation discount planning
   - GRAT structures for family succession
   - Intentionally defective grantor trusts (IDGTs)
   - Key employee retention

6. RISK MANAGEMENT
   - Entity liability protection
   - Key person insurance
   - Business overhead expense insurance
   - Directors & Officers coverage
   - Umbrella liability
```

### Prompt 2E: Estate & Wealth Transfer Planning

Use this for estate planning, especially with cross-border elements:

```
I need guidance on estate and wealth transfer planning.

MY SITUATION:
- Tax residency: [COUNTRY]
- Citizenship: [CITIZENSHIP(S)]
- Domicile (for estate tax): [COUNTRY]
- Family situation: [MARRIED/SINGLE], [NUMBER] children, [OTHER DEPENDENTS]
- Approximate net worth range: [RANGE]
- Primary asset types: [REAL ESTATE / SECURITIES / BUSINESS / OTHER]
- Cross-border assets: [YES/NO - LOCATIONS]

Please advise on:

1. ESTATE TAX FRAMEWORK
   - Estate/inheritance tax rates and thresholds
   - Marital deduction or spousal exemption
   - Lifetime gift tax exemption and annual exclusions
   - Generation-skipping transfer tax
   - State/provincial estate taxes (if applicable)

2. CROSS-BORDER ESTATE ISSUES
   - Situs rules for different asset types
   - Treaty estate tax provisions
   - Forced heirship rules
   - Recognition of foreign wills and trusts
   - Probate in multiple jurisdictions

3. WEALTH TRANSFER STRATEGIES
   - Annual exclusion gifting programs
   - 529 plan superfunding
   - Grantor retained annuity trusts (GRATs)
   - Spousal lifetime access trusts (SLATs)
   - Irrevocable life insurance trusts (ILITs)
   - Family limited partnerships/LLCs

4. TRUST STRUCTURES
   - Revocable vs irrevocable trusts
   - Grantor vs non-grantor trust status
   - Dynasty/perpetual trusts
   - Foreign trust rules and reporting
   - Trust situs selection

5. CHARITABLE PLANNING
   - Donor-advised funds
   - Private foundations
   - Charitable remainder trusts
   - Charitable lead trusts
   - Qualified charitable distributions

6. DOCUMENTS NEEDED
   - Will structure for multi-jurisdictional assets
   - Power of attorney (financial and healthcare)
   - Healthcare directives
   - Trust documents
   - Beneficiary designation review
```

### Prompt 2F: Risk Management & Insurance Review

Use this for comprehensive insurance planning:

```
I need a comprehensive review of risk management and insurance needs.

MY SITUATION:
- Tax residency: [COUNTRY]
- Age: [AGE BRACKET]
- Family: [MARITAL STATUS, DEPENDENTS]
- Income: [RANGE]
- Net worth: [RANGE]
- Occupation: [ROLE AND INDUSTRY]
- Health status: [STANDARD / SPECIFIC CONDITIONS]

Please advise on:

1. LIFE INSURANCE NEEDS
   - Income replacement calculation methodology
   - Term vs permanent insurance analysis
   - Policy amount and term recommendations
   - Ownership structure (individual vs trust)
   - Cross-border life insurance issues

2. DISABILITY INSURANCE
   - Own-occupation vs any-occupation coverage
   - Benefit period and elimination period
   - Group vs individual policy analysis
   - Residual/partial disability riders
   - Cost-of-living adjustment riders

3. HEALTH INSURANCE
   - Coverage gaps analysis
   - International health insurance for mobile individuals
   - Long-term care planning
   - HSA/FSA optimization

4. LIABILITY PROTECTION
   - Umbrella insurance sizing
   - Professional liability (E&O, malpractice)
   - Directors & Officers coverage
   - Cyber liability

5. PROPERTY PROTECTION
   - Homeowners/renters coverage adequacy
   - Valuable articles scheduling
   - Business property coverage

6. TAX-ADVANTAGED INSURANCE STRATEGIES
   - Cash value life insurance for tax-deferred growth
   - Life insurance as alternative to bonds
   - Premium financing considerations
   - Section 79 plans
```

### Prompt 2G: Specific Scenario Analysis

Use this for specific questions not covered above:

```
I have a specific financial planning question.

MY SITUATION:
[PASTE RELEVANT SECTIONS FROM YOUR SITUATION PROFILE]

CONTEXT:
[RELEVANT BACKGROUND FOR THIS QUESTION]

MY SPECIFIC QUESTION:
[YOUR QUESTION - be as specific as possible]

Please provide:

1. DIRECT ANSWER
   - Clear recommendation with reasoning

2. KEY FACTORS
   - Variables that affect the answer
   - Assumptions made

3. QUANTITATIVE ANALYSIS (if applicable)
   - Numbers, rates, thresholds involved
   - Break-even points or decision criteria

4. RISKS & CONSIDERATIONS
   - Potential downsides
   - What could change this analysis

5. IMPLEMENTATION STEPS
   - Specific next actions
   - Timeline considerations
   - Professional help needed

6. WHAT YOU MIGHT BE MISSING
   - Related issues to consider
   - Questions to ask professionals
```

---

## Part 3: Use the Calculator Tool

Test your numbers using Monte Carlo simulation.

### Input Mapping

| Calculator Field | What to Enter | Source |
|------------------|---------------|--------|
| Current Savings | Assets allocated to THIS goal | Your records |
| Target Amount | Goal amount in today's purchasing power | Section G |
| Years | Timeline to goal | Section G |
| Monthly Contribution | Sustainable monthly savings for this goal | Your budget |
| Risk Profile | Based on timeline and flexibility | See below |

### Risk Profile Selection

| Profile | Expected Return | Volatility | Appropriate When |
|---------|-----------------|------------|------------------|
| Conservative | 6% | 10% | Timeline <5 years, or fixed deadline |
| Moderate | 8% | 13% | Timeline 5-15 years, some flexibility |
| Aggressive | 10% | 16% | Timeline 15+ years, high flexibility |
| Very Aggressive | 12% | 20% | Timeline 20+ years, maximum flexibility |

### Interpreting Results

| Success Probability | Assessment | Action |
|---------------------|------------|--------|
| 80%+ (Green) | On track | Maintain current plan |
| 50-79% (Yellow) | Stretch goal | Increase contribution, extend timeline, or accept risk |
| <50% (Red) | Needs adjustment | Significant changes required |

### Record Results

```
CALCULATOR RESULTS
==================

Goal 1: _______________
  Inputs: $_______ current → $_______ target over _____ years
          $_______ /month, _______ risk profile
  Results:
    - Success probability: _______% [GREEN/YELLOW/RED]
    - Required return: _______%
    - 10th percentile outcome: $_______
    - Median outcome: $_______
  Assessment: _______________

Goal 2: _______________
  [Same format]

Goal 3: _______________
  [Same format]

TOTAL MONTHLY SAVINGS REQUIRED: $_______
TOTAL AS % OF GROSS INCOME: _______%
```

---

## Part 4: Assemble Your Plan

Synthesize research and calculator results into an actionable plan.

```
FINANCIAL PLAN
==============
Prepared: [DATE]
Next review: [DATE + 6 MONTHS]

EXECUTIVE SUMMARY
-----------------
Primary residence: [COUNTRY]
Citizenship: [CITIZENSHIP(S)]
Planning horizon: [YEARS TO PRIMARY GOAL]
Mobility: [ANCHORED / MOBILE]
Overall assessment: [ON TRACK / ADJUSTMENTS NEEDED / SIGNIFICANT CHANGES REQUIRED]

ACCOUNT STRATEGY
----------------
Tax-advantaged accounts (prioritized):
1. [ACCOUNT TYPE]: $____/month
   - Rationale: [WHY THIS ACCOUNT]
   - Contribution limit: $____/year
   - Tax benefit: [DESCRIPTION]

2. [ACCOUNT TYPE]: $____/month
   - Rationale: [WHY]
   - Contribution limit: $____/year
   - Tax benefit: [DESCRIPTION]

Taxable accounts:
- Brokerage: $____/month
  - Purpose: [PORTABILITY / LIQUIDITY / OVERFLOW]
  - Tax-efficiency approach: [TAX-LOSS HARVESTING / INDEX FUNDS / ETF DOMICILE]

Accounts NOT using and why:
- [ACCOUNT]: [REASON - e.g., not portable, already maxed, not eligible]

GOAL FUNDING ALLOCATION
-----------------------
Total monthly savings: $_______ (____% of gross income)

Goal 1: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Account: [WHERE FUNDS GO]
  Monthly: $_______
  Probability: _______%

Goal 2: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Account: [WHERE FUNDS GO]
  Monthly: $_______
  Probability: _______%

Goal 3: [NAME] — [GREEN/YELLOW/RED]
  Target: $_______ by [YEAR]
  Account: [WHERE FUNDS GO]
  Monthly: $_______
  Probability: _______%

EQUITY COMPENSATION STRATEGY (if applicable)
--------------------------------------------
Current holdings: [DESCRIPTION]
Diversification plan: [STRATEGY]
Tax optimization: [APPROACH]
Timeline: [WHEN ACTIONS OCCUR]

RISK MANAGEMENT
---------------
Life insurance: [AMOUNT, TYPE, OWNER]
Disability insurance: [COVERAGE DETAILS]
Umbrella liability: [AMOUNT]
Gaps identified: [ANY COVERAGE GAPS]

ESTATE PLANNING STATUS
----------------------
Will: [CURRENT / NEEDS UPDATE / NONE]
Trusts: [DESCRIPTION IF ANY]
Beneficiary designations: [REVIEWED DATE]
Power of attorney: [IN PLACE / NEEDED]
Healthcare directive: [IN PLACE / NEEDED]

CONTINGENCY PLANS
-----------------
If I relocate to [COUNTRY]:
  - Accounts affected: [LIST]
  - Actions needed: [STEPS]
  - Tax implications: [SUMMARY]

If income decreases significantly:
  - Priority reduction: [WHICH GOALS FLEX]
  - Emergency reserves: [MONTHS COVERAGE]

If income increases significantly:
  - Additional contributions to: [WHERE]
  - New opportunities: [WHAT OPENS UP]

COMPLIANCE CHECKLIST
--------------------
[ ] Employer match fully captured
[ ] All required tax filings identified (FBAR, FATCA, CRS, etc.)
[ ] Account beneficiaries current
[ ] Insurance policies reviewed annually
[ ] Estate documents valid in current jurisdiction

OPEN QUESTIONS FOR PROFESSIONAL REVIEW
--------------------------------------
- [QUESTION 1 - for tax advisor]
- [QUESTION 2 - for estate attorney]
- [QUESTION 3 - for financial planner]

REVIEW TRIGGERS
---------------
Re-evaluate this plan when:
[ ] Job change or major income change (>20%)
[ ] Relocation to different jurisdiction
[ ] Marriage, divorce, or children
[ ] Major asset acquisition (real estate, business)
[ ] Every 12 months regardless
[ ] Tax law changes affecting your situation
```

---

## Part 5: Plan Validation

Before finalizing, validate your plan:

```
Please review my financial plan for internal consistency, gaps, and potential issues.
Do NOT provide a new plan—identify issues with MY plan.

MY SITUATION PROFILE:
[PASTE COMPLETED PROFILE FROM PART 1]

MY RESEARCH FINDINGS:
[PASTE KEY FINDINGS FROM PART 2 PROMPTS]

MY PLAN:
[PASTE COMPLETED PLAN FROM PART 4]

CALCULATOR RESULTS:
[PASTE RESULTS FROM PART 3]

Please evaluate:

1. MATHEMATICAL CONSISTENCY
   - Do contributions sum correctly?
   - Is savings rate sustainable for stated income level?
   - Do calculator probabilities align with stated risk tolerance?
   - Are contribution limits respected?

2. ACCOUNT OPTIMIZATION
   - Am I maximizing tax-advantaged space appropriately?
   - Given my mobility, is the portable/locked allocation correct?
   - Are there account types I should consider but haven't?
   - Is the investment approach tax-efficient?

3. GOAL PRIORITIZATION
   - Is the funding order appropriate?
   - Are critical foundations in place (emergency fund, debt, insurance)?
   - Do goal timelines align with account access rules?

4. RISK ASSESSMENT
   - Does risk profile match timeline and flexibility?
   - Is concentration risk addressed?
   - Are insurance coverages adequate?
   - Are contingency plans realistic?

5. CROSS-BORDER CONSISTENCY (if applicable)
   - Do account choices align with stated mobility?
   - Are compliance requirements identified?
   - Is exit tax exposure considered?
   - Are treaty benefits correctly applied?

6. GAPS & OVERSIGHTS
   - What am I not thinking about?
   - What questions should I ask professionals?
   - What could derail this plan?
   - What assumptions need monitoring?

Be direct and specific. Flag anything that doesn't make sense.
```

---

## Quick Reference: Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. COMPLETE SITUATION PROFILE (Part 1)                          │
│    → Be thorough—this determines which prompts you need         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 2. RESEARCH YOUR JURISDICTION (Part 2)                          │
│    → Start with 2A (everyone)                                   │
│    → Add 2B if mobile, 2C if equity comp, 2D if business owner  │
│    → 2E for estate planning, 2F for insurance review            │
│    → 2G for specific questions                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. TEST YOUR NUMBERS (Part 3)                                   │
│    → Monte Carlo simulation for each goal                       │
│    → Adjust until GREEN or acceptable YELLOW                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 4. ASSEMBLE YOUR PLAN (Part 4)                                  │
│    → Synthesize research + calculator into actionable plan      │
│    → Specify accounts, amounts, contingencies                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 5. VALIDATE (Part 5)                                            │
│    → Check for internal consistency and gaps                    │
│    → Identify questions for professionals                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ 6. IMPLEMENT & MONITOR                                          │
│    → Execute account openings and contributions                 │
│    → Set up automations                                         │
│    → Calendar review triggers                                   │
│    → Engage professionals for complex items                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## When to Engage Professionals

This framework facilitates self-directed planning, but some situations require professional guidance:

**Tax Advisor / CPA:**
- Cross-border income or assets
- Equity compensation strategies
- Business tax optimization
- Audit support

**Estate Planning Attorney:**
- Trusts and complex structures
- Multi-jurisdictional assets
- Business succession
- Family wealth transfer

**Financial Planner (CFP):**
- Comprehensive plan review
- Insurance analysis
- Investment policy development
- Retirement income planning

**Immigration Attorney:**
- Visa implications for financial planning
- Expatriation planning
- Citizenship planning

---

## Disclaimer

This framework is for educational purposes only. It does not constitute financial, tax, legal, or investment advice. The prompts generate general information that may not apply to your specific situation.

- Tax laws change frequently; verify current rules
- Cross-border situations are particularly complex
- Past performance does not guarantee future results
- Individual circumstances vary significantly

Always consult qualified professionals before making significant financial decisions.
