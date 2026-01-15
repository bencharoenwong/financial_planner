# Financial Goal Analyzer

A free, open-source web app that helps users determine if their financial goals are achievable using deterministic mathematical models—no AI, no hallucinations, just transparent math.

## 🚀 Quick Start

### Run Locally

```bash
# 1. Clone/download files
# 2. Install dependencies
pip install fastapi uvicorn numpy scipy pydantic

# 3. Start the API server
uvicorn api:app --reload --port 8000

# 4. Open index.html in your browser (or serve it)
python -m http.server 3000  # Then visit http://localhost:3000
```

### Run with Docker

```bash
docker build -t financial-analyzer .
docker run -p 8000:8000 financial-analyzer
```

## 📁 Files

| File | Purpose |
|------|---------|
| `SPEC.md` | Complete specification for Claude Code |
| `api.py` | FastAPI backend (production-ready) |
| `index.html` | Single-page frontend (no build required) |
| `financial_goal_analyzer.py` | CLI tool for batch CSV processing |
| `requirements.txt` | Python dependencies |
| `vercel.json` | Vercel deployment config |

## 🤖 Claude Code Commands

Use these prompts with Claude Code to extend or deploy the project:

### Deploy to Vercel
```
Deploy this financial analyzer to Vercel. Set up the Python API as serverless functions and the index.html as the static frontend. Configure CORS properly.
```

### Add Database (Optional)
```
Add PostgreSQL integration to save analysis results. Create a /api/history endpoint to retrieve past analyses. Use SQLAlchemy with async support.
```

### Add User Authentication
```
Add Clerk or Auth0 authentication. Protect the /api/analyze endpoint with rate limiting for unauthenticated users (10/hour) and unlimited for authenticated.
```

### Build React Frontend
```
Convert index.html to a Next.js 14 app with TypeScript. Use shadcn/ui components. Add Recharts for the wealth projection visualization. Keep the same API contract.
```

### Add Email Reports
```
Add a /api/report endpoint that generates a PDF summary of the analysis and emails it to the user using Resend or SendGrid.
```

### Integrate with n8n
```
Create an n8n workflow that:
1. Triggers on Google Form submission
2. Calls /api/analyze with the form data
3. Routes by status (GREEN/YELLOW/RED)
4. Sends Slack notification for RED status
5. Saves all results to Google Sheets
```

## 📊 API Reference

### POST /api/analyze

Analyze a financial goal.

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
  "probabilityOfSuccess": 0.524,
  "requiredMonthlyFor80Percent": 881.27,
  "contributionGap": 381.27,
  "projections": {
    "percentile20": 603527,
    "percentile50": 1040509,
    "percentile80": 1839640
  },
  "status": "RED",
  "flags": ["Success probability 52% below 80% threshold"],
  "recommendations": ["Increase monthly contribution by $381"]
}
```

### GET /api/profiles

Get available risk profiles and their assumptions.

### GET /api/health

Health check endpoint.

## 🎯 Risk Profiles

| Profile | Return | Volatility | Description |
|---------|--------|------------|-------------|
| Conservative | 6% | 10% | Bond-heavy (70/30) |
| Moderate | 8% | 13% | Balanced (40/60) |
| Aggressive | 10% | 16% | S&P 500-like |
| Very Aggressive | 12% | 20% | Concentrated |

## 🚦 Status Flags

| Status | Criteria |
|--------|----------|
| 🟢 GREEN | ≥80% success probability |
| 🟡 YELLOW | 50-79% success probability |
| 🔴 RED | <50% success probability |

Additional flags trigger for:
- Required savings >20% of income (warning)
- Required savings >35% of income (critical)
- Required return >12% (aggressive)
- Required return >15% (unrealistic)

## 🧮 Methodology

1. **Market Returns**: Uses historical equity/bond return assumptions
2. **Volatility Adjustment**: Converts arithmetic to geometric returns
3. **Lump Sum**: Log-normal distribution for pure investment growth
4. **With Contributions**: Monte Carlo simulation (15,000 paths)
5. **Required Monthly**: Binary search for 80% success threshold

All calculations are deterministic given the same inputs and random seed.

## 📄 License

MIT License - free to use, modify, and distribute.

## 🏢 Attribution

Built by Chicago Global Capital - Parallax Team

---

## CLI Usage (Batch Processing)

For processing multiple clients via CSV:

```bash
# Generate sample input
python financial_goal_analyzer.py --sample clients.csv

# Run analysis
python financial_goal_analyzer.py clients.csv results.csv

# With custom thresholds
python financial_goal_analyzer.py clients.csv results.csv --config config.json
```

### CSV Input Format

```csv
client_id,current_wealth,target_wealth,years,monthly_contribution,risk_profile,monthly_income
CLIENT_001,10000,1000000,30,500,aggressive,8000
CLIENT_002,50000,500000,20,1000,moderate,10000
```

### CSV Output Includes

- All input fields echoed
- Success probability
- Percentile projections (20th, 50th, 80th)
- Required monthly for 80% success
- Contribution gap
- Status flag (GREEN/YELLOW/RED)
- Flag reasons
- Recommendations
