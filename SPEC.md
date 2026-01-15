# Financial Goal Feasibility Analyzer - Project Specification

> **For use with Claude Code** - This spec defines a free web application that helps users determine if their financial goals are realistic and what adjustments they need to make.

## Project Overview

### Purpose
A deterministic financial planning tool that analyzes whether a user's wealth accumulation goal is achievable given their starting capital, time horizon, savings rate, and risk tolerance. Unlike AI-based advice, this tool uses fixed mathematical models with configurable assumptions, making outputs predictable and auditable.

### Target Users
- Retail investors planning for retirement, home purchase, or other goals
- Financial advisors doing quick feasibility checks
- Fintech apps needing a white-label planning API

### Key Value Proposition
- **No AI hallucination** - Pure math with transparent assumptions
- **Instant results** - No waiting for model inference
- **Free tier** - Basic analysis at no cost
- **API available** - For integration into other apps

---

## Technical Architecture

### Stack (Recommended)
```
Frontend:  React + TypeScript + Tailwind CSS (or Next.js for SSR)
Backend:   FastAPI (Python) or Next.js API routes
Compute:   NumPy, SciPy for calculations
Database:  Optional - PostgreSQL for saving analyses (or stateless)
Hosting:   Vercel / Railway / Render (free tier compatible)
```

### Alternative Lightweight Stack
```
Single Page:  HTML + Alpine.js + Chart.js
Backend:      Python FastAPI or Flask
Hosting:      Vercel serverless functions / Railway
```

---

## Data Models

### Input Schema
```typescript
interface FinancialGoalInput {
  // Required fields
  currentWealth: number;        // Starting capital ($), must be > 0
  targetWealth: number;         // Goal amount ($), must be > 0
  yearsToGoal: number;          // Time horizon, 1-50 years
  monthlyContribution: number;  // Planned monthly savings ($), >= 0
  
  // Optional fields
  riskProfile?: 'conservative' | 'moderate' | 'aggressive' | 'very_aggressive';
  monthlyIncome?: number;       // For sustainability analysis ($)
  inflationAdjusted?: boolean;  // Return real vs nominal projections
}
```

### Output Schema
```typescript
interface AnalysisResult {
  // Input echo
  input: FinancialGoalInput;
  
  // Market assumptions used
  assumptions: {
    arithmeticReturn: number;   // e.g., 0.10 for 10%
    geometricReturn: number;    // e.g., 0.0872
    volatility: number;         // e.g., 0.16 for 16%
    riskProfile: string;
  };
  
  // Core results
  probabilityOfSuccess: number;           // 0-1, with current plan
  requiredMonthlyFor80Percent: number;    // $ needed for 80% success
  contributionGap: number;                // Difference from current
  
  // Wealth distribution projections
  projections: {
    percentile20: number;   // 80% chance of beating this (floor)
    percentile50: number;   // Median outcome
    percentile80: number;   // 20% chance of beating this (ceiling)
  };
  
  // Lump sum only (for reference)
  lumpSumOnly: {
    probabilityOfSuccess: number;
    percentile20: number;
    percentile50: number;
    percentile80: number;
  };
  
  // Flags and recommendations
  status: 'GREEN' | 'YELLOW' | 'RED';
  flags: string[];
  recommendations: string[];
  
  // Metadata
  analyzedAt: string;  // ISO timestamp
  version: string;     // API version
}
```

### Risk Profile Assumptions
```typescript
const RISK_PROFILES = {
  conservative: {
    arithmeticReturn: 0.06,
    volatility: 0.10,
    description: "Bond-heavy allocation (e.g., 70% bonds, 30% stocks)"
  },
  moderate: {
    arithmeticReturn: 0.08,
    volatility: 0.13,
    description: "Balanced allocation (e.g., 40% bonds, 60% stocks)"
  },
  aggressive: {
    arithmeticReturn: 0.10,
    volatility: 0.16,
    description: "Equity-focused (e.g., S&P 500 index)"
  },
  very_aggressive: {
    arithmeticReturn: 0.12,
    volatility: 0.20,
    description: "Concentrated/leveraged positions"
  }
};
```

### Flag Thresholds (Configurable)
```typescript
const THRESHOLDS = {
  successProbGreen: 0.80,      // >= 80% = on track
  successProbYellow: 0.50,     // >= 50% = needs attention
  // Below 50% = critical (RED)
  
  contributionWarningPct: 0.20,   // > 20% of income = warning
  contributionCriticalPct: 0.35, // > 35% of income = unsustainable
  
  requiredReturnWarning: 0.12,   // > 12% = aggressive
  requiredReturnCritical: 0.15,  // > 15% = unrealistic
};
```

---

## Core Calculation Logic

### Step 1: Geometric Return Conversion
```python
geometric_return = arithmetic_return - (volatility ** 2) / 2
```

### Step 2: Lump Sum Distribution (Log-Normal)
For a lump sum investment, terminal wealth follows a log-normal distribution:
```python
mean_log_wealth = ln(initial) + years * geometric_return
std_log_wealth = volatility * sqrt(years)

percentile_X = exp(mean_log_wealth + z_X * std_log_wealth)
# where z_X is the standard normal quantile (e.g., z_20 ≈ -0.842)
```

### Step 3: Probability of Success (Lump Sum)
```python
z_target = (ln(target) - mean_log_wealth) / std_log_wealth
prob_success = 1 - norm.cdf(z_target)
```

### Step 4: Monte Carlo for Contributions
Monthly DCA requires simulation (no closed-form solution):
```python
def simulate(initial, monthly_contrib, years, arith_return, volatility, n_sims=20000):
    monthly_return = arith_return / 12
    monthly_vol = volatility / sqrt(12)
    months = years * 12
    
    # Generate random returns: shape (n_sims, months)
    returns = np.random.normal(monthly_return, monthly_vol, (n_sims, months))
    
    # Compound wealth with contributions
    wealth = np.full(n_sims, initial)
    for t in range(months):
        wealth = (wealth + monthly_contrib) * (1 + returns[:, t])
    
    return wealth  # Final wealth distribution
```

### Step 5: Binary Search for Required Contribution
```python
def find_required_monthly(initial, target, years, arith_return, volatility, target_prob=0.80):
    low, high = 0, target / (years * 12)
    
    for _ in range(20):  # 20 iterations = ~1e-6 precision
        mid = (low + high) / 2
        prob = simulate_success_rate(initial, target, years, mid, arith_return, volatility)
        if prob < target_prob:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2
```

### Step 6: Flag Determination
```python
def determine_status(prob_success, required_monthly, monthly_income, required_cagr):
    flags = []
    status = "GREEN"
    
    # Check success probability
    if prob_success < 0.50:
        status = "RED"
        flags.append(f"Success probability {prob_success:.0%} critically low")
    elif prob_success < 0.80:
        status = "YELLOW"
        flags.append(f"Success probability {prob_success:.0%} below 80% threshold")
    
    # Check contribution sustainability
    if monthly_income and monthly_income > 0:
        ratio = required_monthly / monthly_income
        if ratio > 0.35:
            status = "RED"
            flags.append(f"Required savings {ratio:.0%} of income unsustainable")
        elif ratio > 0.20:
            status = max(status, "YELLOW")  # Don't downgrade RED
            flags.append(f"Required savings {ratio:.0%} of income is high")
    
    # Check required return
    if required_cagr > 0.15:
        status = "RED"
        flags.append(f"Required return {required_cagr:.0%} exceeds realistic expectations")
    elif required_cagr > 0.12:
        status = max(status, "YELLOW")
        flags.append(f"Required return {required_cagr:.0%} is aggressive")
    
    return status, flags
```

---

## API Endpoints

### POST /api/analyze
Main analysis endpoint.

**Request:**
```json
{
  "currentWealth": 10000,
  "targetWealth": 1000000,
  "yearsToGoal": 30,
  "monthlyContribution": 500,
  "riskProfile": "aggressive",
  "monthlyIncome": 8000
}
```

**Response:**
```json
{
  "input": { ... },
  "assumptions": {
    "arithmeticReturn": 0.10,
    "geometricReturn": 0.0872,
    "volatility": 0.16,
    "riskProfile": "aggressive"
  },
  "probabilityOfSuccess": 0.524,
  "requiredMonthlyFor80Percent": 881.27,
  "contributionGap": 381.27,
  "projections": {
    "percentile20": 603527,
    "percentile50": 1040509,
    "percentile80": 1839640
  },
  "lumpSumOnly": {
    "probabilityOfSuccess": 0.012,
    "percentile20": 65433,
    "percentile50": 136809,
    "percentile80": 286044
  },
  "status": "RED",
  "flags": [
    "Success probability 52% below 80% threshold",
    "Required return 17% exceeds realistic expectations"
  ],
  "recommendations": [
    "CRITICAL: Current goal is not achievable with stated parameters.",
    "Realistic target at 80% confidence: $603,527",
    "Consider extending timeline beyond 30 years if possible.",
    "Sustainable monthly savings at your income: $1,600"
  ],
  "analyzedAt": "2026-01-14T12:00:00Z",
  "version": "1.0.0"
}
```

### POST /api/analyze/batch
Batch analysis for CSV upload.

**Request:** `multipart/form-data` with CSV file

**Response:** JSON array of AnalysisResult objects or CSV download

### GET /api/profiles
Return available risk profiles and their assumptions.

### GET /api/health
Health check endpoint.

---

## Frontend UI Components

### Main Calculator Form
```
┌─────────────────────────────────────────────────────────────┐
│  💰 Financial Goal Analyzer                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Current Savings        Target Goal                         │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ $  10,000       │    │ $  1,000,000    │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  Time Horizon           Monthly Contribution                │
│  ┌─────────────────┐    ┌─────────────────┐                │
│  │ 30 years        │    │ $  500          │                │
│  └─────────────────┘    └─────────────────┘                │
│                                                             │
│  Risk Profile                                               │
│  ○ Conservative (6% return, low volatility)                │
│  ○ Moderate (8% return, balanced)                          │
│  ● Aggressive (10% return, S&P 500-like)                   │
│  ○ Very Aggressive (12% return, high volatility)           │
│                                                             │
│  Monthly Income (optional, for sustainability check)        │
│  ┌─────────────────┐                                       │
│  │ $  8,000        │                                       │
│  └─────────────────┘                                       │
│                                                             │
│              ┌──────────────────────┐                      │
│              │   Analyze My Goal    │                      │
│              └──────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

### Results Display
```
┌─────────────────────────────────────────────────────────────┐
│  📊 Analysis Results                          🔴 RED STATUS │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Success Probability: 52%                                   │
│  ████████████░░░░░░░░░░░░ (need 80%+)                      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ PROJECTED OUTCOMES (with $500/mo contributions)     │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ Worst case (80% beat):     $603,527                 │   │
│  │ Median outcome:            $1,040,509               │   │
│  │ Best case (20% beat):      $1,839,640               │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💡 To reach 80% success:                                   │
│     Increase contribution to $881/month (+$381)             │
│                                                             │
│  ⚠️ Flags:                                                  │
│  • Success probability 52% below 80% threshold              │
│  • Required return 17% exceeds realistic expectations       │
│                                                             │
│  📋 Recommendations:                                        │
│  • Realistic target at 80% confidence: $603,527             │
│  • Consider extending timeline beyond 30 years              │
│  • Sustainable savings at your income: $1,600/mo            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visualization: Wealth Projection Chart
Show fan chart with percentile bands over time:
- X-axis: Years (0 to goal)
- Y-axis: Wealth ($)
- Bands: 20th-80th percentile shaded, median line, target line

---

## File Structure

```
financial-goal-analyzer/
├── README.md
├── SPEC.md                    # This file
├── package.json               # or pyproject.toml
│
├── frontend/                  # React/Next.js frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── CalculatorForm.tsx
│   │   │   ├── ResultsDisplay.tsx
│   │   │   ├── WealthChart.tsx
│   │   │   ├── StatusBadge.tsx
│   │   │   └── RiskProfileSelector.tsx
│   │   ├── pages/
│   │   │   ├── index.tsx      # Main calculator
│   │   │   ├── api/           # API routes (if Next.js)
│   │   │   └── batch.tsx      # CSV upload page
│   │   ├── lib/
│   │   │   ├── types.ts       # TypeScript interfaces
│   │   │   └── api.ts         # API client
│   │   └── styles/
│   └── public/
│
├── backend/                   # FastAPI backend (if separate)
│   ├── main.py                # FastAPI app
│   ├── analyzer.py            # Core calculation engine
│   ├── models.py              # Pydantic models
│   ├── config.py              # Thresholds and assumptions
│   └── requirements.txt
│
├── core/                      # Shared calculation logic
│   └── financial_goal_analyzer.py  # The script we already built
│
├── tests/
│   ├── test_analyzer.py
│   └── test_api.py
│
└── deployment/
    ├── Dockerfile
    ├── vercel.json
    └── railway.toml
```

---

## Deployment Options

### Option 1: Vercel (Recommended for free tier)
- Frontend: Automatic from Next.js
- Backend: Serverless Python functions
- Limitations: 10s function timeout, 50MB bundle

```json
// vercel.json
{
  "functions": {
    "api/*.py": {
      "runtime": "python3.11",
      "maxDuration": 10
    }
  }
}
```

### Option 2: Railway
- Full Python backend support
- $5 free credit/month
- Better for heavier computation

### Option 3: Render
- Free tier for static sites
- Free tier for web services (spins down after inactivity)

### Option 4: Self-hosted
- Any VPS with Docker
- Use provided Dockerfile

---

## Claude Code Commands

Use these commands with Claude Code to build the project:

### Initialize Project
```
Create a new Next.js project with TypeScript and Tailwind CSS for a financial goal analyzer web app. Use the app router. Set up the project structure as defined in SPEC.md.
```

### Implement Backend
```
Create a FastAPI backend in /backend that implements the /api/analyze endpoint. Port the calculation logic from financial_goal_analyzer.py. Use Pydantic for request/response validation.
```

### Implement Frontend
```
Build the calculator form component with inputs for currentWealth, targetWealth, yearsToGoal, monthlyContribution, riskProfile, and monthlyIncome. Add client-side validation. Style with Tailwind.
```

### Add Visualization
```
Create a WealthChart component using Recharts that shows projected wealth over time with percentile bands (20th, 50th, 80th). Include the target line and current trajectory.
```

### Deploy
```
Set up deployment configuration for Vercel. Create vercel.json and any necessary API route handlers. Ensure the Python calculation engine works as a serverless function.
```

### Add Tests
```
Write pytest tests for the analyzer module covering: normal inputs, edge cases (0 contribution, very short/long horizons), flag determination logic, and Monte Carlo convergence.
```

---

## Testing Scenarios

### Happy Path
- $100K → $500K in 20 years, $1K/month, moderate risk
- Expected: GREEN status, ~85% success

### Edge Cases
1. **Zero contribution**: Should still work (lump sum only)
2. **Very short horizon**: 1-5 years, high uncertainty
3. **Very long horizon**: 40+ years, compounding dominates
4. **Impossible goal**: $1K → $10M in 5 years, should be RED
5. **Already achieved**: Current >= target, should be GREEN

### Validation
- All dollar amounts must be positive
- Years must be 1-50
- Monthly contribution >= 0
- Risk profile must be valid enum

---

## Future Enhancements (v2)

- [ ] Inflation adjustment toggle
- [ ] Tax-advantaged account modeling (401k, IRA limits)
- [ ] Social Security integration
- [ ] Multiple goals (retirement + house + education)
- [ ] Scenario comparison (side-by-side)
- [ ] PDF report generation
- [ ] Email results
- [ ] Save/load analyses (requires auth)
- [ ] Employer match calculator
- [ ] Withdrawal phase modeling (decumulation)

---

## Legal Disclaimers (Include in UI)

```
DISCLAIMER: This tool provides educational estimates only and does not 
constitute financial advice. Projections are based on historical market 
assumptions and do not guarantee future results. Past performance is not 
indicative of future returns. Consult a qualified financial advisor before 
making investment decisions. [Your Company] is not responsible for any 
financial decisions made based on this tool's output.
```

---

## License

MIT License - Free to use, modify, and distribute.

---

## Contact / Support

For questions about this spec or implementation assistance:
- Create an issue in the repository
- Email: [your-email]

---

*Spec Version: 1.0.0*
*Last Updated: January 2026*
*Author: Chicago Global Capital - Parallax Team*
