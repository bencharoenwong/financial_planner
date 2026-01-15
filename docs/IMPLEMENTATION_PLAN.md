# Implementation Plan: Option A (Calculator)

> Ship a clean, lightweight financial goal feasibility calculator.

---

## Scope

**In scope:**
- Monte Carlo goal analysis (already built)
- CSV batch upload via API
- Clean, deduplicated codebase
- Local storage for saved scenarios (frontend)

**Out of scope:**
- User accounts
- Bank linking
- Gamification
- Daily engagement features

---

## Phase 1: Code Cleanup (Before First Commit)

### 1.1 Deduplicate Calculation Engine

**Problem:** `api.py` and `financial_goal_analyzer.py` have independent implementations (~200 lines duplicated).

**Solution:**
```
core/
├── __init__.py
├── engine.py      # FinancialAnalyzer class (single source of truth)
├── models.py      # Dataclasses (AnalysisResult, ThresholdConfig, etc.)
└── config.py      # Risk profiles, thresholds
```

Both `api.py` and `financial_goal_analyzer.py` will import from `core/`.

### 1.2 Fix Deprecations

- Update Pydantic `schema_extra` → `model_config` (v2 pattern)
- Clean up any other deprecation warnings

### 1.3 Add Tests

Basic pytest coverage:
- `tests/test_engine.py` - Calculation logic
- `tests/test_api.py` - API endpoints

### 1.4 Security Tightening

- Make CORS configurable via environment variable
- Add rate limiting consideration for production

---

## Phase 2: Batch API Endpoint

### 2.1 Implement `/api/analyze/batch`

```python
@app.post("/api/analyze/batch")
async def analyze_batch(file: UploadFile = File(...)):
    """Accept CSV, return JSON array of results."""
```

**Input:** CSV with columns matching single analysis
**Output:** JSON array of AnalysisResponse objects

### 2.2 Add CSV Download Option

Query param or Accept header to return CSV instead of JSON.

---

## Phase 3: Frontend Enhancements

### 3.1 Local Storage Scenarios

- Save up to 5 scenarios in localStorage
- Name/rename scenarios
- Delete scenarios
- Auto-save last analysis

### 3.2 Comparison View

- Side-by-side view of 2-3 scenarios
- Highlight differences (contribution gap, probability)

### 3.3 Export

- Export scenario as JSON (for backup/sharing)
- Export results as image (for sharing)

---

## Task Checklist

### Immediate (Code Cleanup)
- [ ] Create `core/` module structure
- [ ] Move calculation logic to `core/engine.py`
- [ ] Move dataclasses to `core/models.py`
- [ ] Move config constants to `core/config.py`
- [ ] Update `api.py` to import from `core/`
- [ ] Update `financial_goal_analyzer.py` to import from `core/`
- [ ] Fix Pydantic deprecations
- [ ] Add `.gitignore` (done)
- [ ] Add basic tests
- [ ] Verify both entry points still work

### Then (Batch API)
- [ ] Implement `/api/analyze/batch` endpoint
- [ ] Add CSV response format option
- [ ] Update API documentation

### Later (Frontend)
- [ ] Add localStorage scenario management
- [ ] Add comparison view
- [ ] Add export functionality

---

## Definition of Done (v1 Ship)

- [ ] Single goal analysis works (web + API)
- [ ] Batch CSV analysis works (API)
- [ ] Code is deduplicated
- [ ] Basic tests pass
- [ ] Deploys to Vercel
- [ ] README is accurate

---

*Plan created: 2026-01-15*
