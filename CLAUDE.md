# Financial Goal Analyzer - Project Instructions

## Overview
Deterministic financial planning tool that analyzes goal feasibility using Monte Carlo simulation. Built for Chicago Global Capital's Parallax product line.

**Current state:** Working calculation engine (API + CLI + web frontend)
**Decision needed:** See `docs/DECISION_SUMMARY.md` for product direction choice

## Documentation

| Document | Purpose |
|----------|---------|
| `SPEC.md` | Technical specification for calculation engine |
| `docs/DECISION_SUMMARY.md` | **START HERE** - Key product direction decision |
| `docs/PRD.md` | Option A: Lightweight calculator (recommended) |
| `docs/PRD_GAMIFICATION.md` | Option B: Duolingo-style gamified experience |
| `docs/COMPETITIVE_ANALYSIS.md` | Why gamification may not transfer to finance |
| `docs/DATA_ARCHITECTURE.md` | Privacy-preserving design (no PII, local storage) |

## Architecture

```
fin_planner/
├── api.py                      # FastAPI backend (REST endpoints)
├── financial_goal_analyzer.py  # CLI tool for batch CSV processing
├── index.html                  # Single-page frontend
├── SPEC.md                     # Technical specification
├── CLAUDE.md                   # This file (project instructions)
├── docs/                       # Product & research docs
│   ├── DECISION_SUMMARY.md     # START HERE - product direction choice
│   ├── PRD.md                  # Option A: Calculator product
│   ├── PRD_GAMIFICATION.md     # Option B: Gamified product
│   ├── COMPETITIVE_ANALYSIS.md # Wealthfront/Duolingo analysis
│   └── DATA_ARCHITECTURE.md    # Privacy-first data design
├── vercel.json                 # Vercel deployment config
├── Dockerfile                  # Container config
└── requirements.txt            # Python dependencies
```

### Key Components

| File | Purpose | Entry Point |
|------|---------|-------------|
| `api.py` | REST API | `uvicorn api:app` |
| `financial_goal_analyzer.py` | CLI batch processing | `python financial_goal_analyzer.py input.csv output.csv` |
| `index.html` | Web UI | Static file, calls `/api/analyze` |

### API Endpoints

- `POST /api/analyze` - Single goal analysis
- `GET /api/profiles` - Risk profile definitions
- `GET /api/health` - Health check

## Known Technical Debt

1. **Code duplication**: `api.py` and `financial_goal_analyzer.py` have independent implementations of the calculation engine. When modifying core logic, update BOTH files or refactor to share code.

2. **Missing batch endpoint**: SPEC defines `/api/analyze/batch` for CSV uploads but not yet implemented.

3. **Frontend fallback**: `index.html` has a simplified JavaScript fallback (`calculateLocally()`) that doesn't match Python accuracy. The JS version uses deterministic approximations instead of Monte Carlo.

## Risk Profile Assumptions

| Profile | Arithmetic Return | Volatility | Description |
|---------|-------------------|------------|-------------|
| conservative | 6% | 10% | Bond-heavy (70/30) |
| moderate | 8% | 13% | Balanced (40/60) |
| aggressive | 10% | 16% | S&P 500-like |
| very_aggressive | 12% | 20% | Concentrated/leveraged |

## Flag Thresholds

- **GREEN**: >= 80% success probability
- **YELLOW**: 50-79% success probability
- **RED**: < 50% success probability

Additional flags:
- Required savings > 20% of income (warning)
- Required savings > 35% of income (critical)
- Required return > 12% (aggressive warning)
- Required return > 15% (unrealistic)

## Development

### Run locally
```bash
# Backend
pip install -r requirements.txt
uvicorn api:app --reload --port 8000

# Frontend (separate terminal)
python -m http.server 3000
# Visit http://localhost:3000
```

### Run CLI tool
```bash
# Generate sample input
python financial_goal_analyzer.py --sample sample_input.csv

# Process batch
python financial_goal_analyzer.py input.csv output.csv
```

### Run with Docker
```bash
docker build -t financial-analyzer .
docker run -p 8000:8000 financial-analyzer
```

## Testing

Tests should cover:
- Normal inputs across all risk profiles
- Edge cases: zero contribution, very short/long horizons
- Flag determination logic
- Monte Carlo convergence (results within expected variance)
- CSV validation and error handling

## Input Validation Rules

| Field | Constraint |
|-------|------------|
| currentWealth | > 0 |
| targetWealth | > 0 |
| yearsToGoal | 1-50 |
| monthlyContribution | >= 0 |
| riskProfile | enum: conservative, moderate, aggressive, very_aggressive |
| monthlyIncome | >= 0 (optional) |

## Deployment

**Vercel**: Configured in `vercel.json`. Python API runs as serverless function.
**Docker**: Use provided `Dockerfile` for self-hosted deployment.

## Product Roadmap

**See `docs/DECISION_SUMMARY.md` for the key decision between two product directions.**

### If Option A (Calculator - Recommended)

Phase 1: Ship current tool
- [x] Monte Carlo simulation engine
- [x] REST API
- [x] Web frontend
- [ ] Code cleanup (deduplicate api.py / financial_goal_analyzer.py)
- [ ] Batch API endpoint for CSV upload

Phase 2: Light engagement
- [ ] Local storage for saved scenarios
- [ ] Side-by-side comparison view
- [ ] Export (JSON/image)

### If Option B (Gamified)

Requires significant additional build. See `docs/PRD_GAMIFICATION.md`.
- [ ] User accounts and database
- [ ] Bank account linking (Plaid)
- [ ] Daily engagement loop
- [ ] XP/streaks/achievements
- [ ] Behavioral inference engine

## Core Data Principle

**We only need summary statistics, not raw transaction data.**

The simulation engine works on aggregates:
- Income bucket (e.g., "75k-100k")
- Expense ratios by category
- Savings rate
- Debt-to-income ratio

Raw transactions, merchant names, exact balances → stay on user's device.

See `docs/DATA_ARCHITECTURE.md` for full design.
