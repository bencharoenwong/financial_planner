# MCP Integration Plan

**Status:** Planned
**Priority:** Next
**Scope:** MCP tool wrapper only (wizard is separate scope)

---

## Overview

Wrap the existing `/api/analyze` endpoint as an MCP tool that allows natural language financial goal queries.

**Pattern:** LLM parses natural language → structured JSON → existing API

```
User: "I have $50k saved, want $1M in 25 years, saving $800/month"
         │
         ▼
    ┌─────────────┐
    │  LLM Layer  │  ← Claude/GPT-4 extracts params using schema
    └──────┬──────┘
           │ {currentWealth: 50000, targetWealth: 1000000, ...}
           ▼
    ┌─────────────┐
    │ /api/analyze│  ← Existing API, no changes needed
    └──────┬──────┘
           ▼
    ┌─────────────┐
    │  Response   │  ← Format for chat context
    │  Formatter  │
    └─────────────┘
```

---

## Files to Create

### 1. `mcp_tool.py` (~150 lines)

```python
"""
MCP Tool Schema for Financial Goal Analyzer

Exposes /api/analyze as an MCP tool with LLM-friendly schema descriptions.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class FinancialGoalInput(BaseModel):
    """
    Analyze whether a financial goal is achievable using Monte Carlo simulation.

    Use this tool when the user wants to:
    - Check if a savings/investment target is achievable
    - Calculate required monthly savings for a goal
    - Evaluate retirement readiness (FIRE)
    - Understand probability of reaching a wealth target
    """

    current_wealth: float = Field(
        ...,
        gt=0,
        description="User's current savings/investments in USD. "
                    "Include: 401k, IRA, brokerage, HSA. "
                    "Exclude: home equity, emergency fund. "
                    "Example: 'I have $50k saved' -> 50000"
    )

    target_wealth: float = Field(
        ...,
        gt=0,
        description="Goal amount in USD. "
                    "For FIRE: annual_expenses × 25 (4% rule). "
                    "Example: 'I want $1 million' -> 1000000"
    )

    years_to_goal: int = Field(
        ...,
        ge=1,
        le=50,
        description="Years until goal. "
                    "Calculate from ages if given. "
                    "Example: 'I'm 35, retire at 60' -> 25"
    )

    monthly_contribution: float = Field(
        ...,
        ge=0,
        description="Monthly savings amount in USD. "
                    "If annual given, divide by 12. "
                    "Example: '$800/month' -> 800"
    )

    risk_profile: Literal[
        "conservative", "moderate", "aggressive", "very_aggressive"
    ] = Field(
        default="moderate",
        description="Investment risk tolerance. Map user language: "
                    "'safe/bonds/low risk' -> conservative (6% return), "
                    "'balanced/mix' -> moderate (8% return), "
                    "'stocks/index funds/S&P' -> aggressive (10% return), "
                    "'crypto/leveraged' -> very_aggressive (12% return). "
                    "Default: moderate if not specified."
    )

    monthly_income: Optional[float] = Field(
        default=None,
        ge=0,
        description="Monthly income for sustainability check (optional). "
                    "If annual salary given, divide by 12. "
                    "Example: '$120k/year' -> 10000. "
                    "Omit if not mentioned."
    )


# MCP Tool Definition
TOOL_DEFINITION = {
    "name": "analyze_financial_goal",
    "description": (
        "Analyze whether a financial goal is achievable. "
        "Returns probability of success, required monthly savings, "
        "projected outcomes, and recommendations. "
        "Use for retirement planning, FIRE, or any wealth accumulation goal."
    ),
    "input_schema": FinancialGoalInput.model_json_schema(),
}


def call_api(params: FinancialGoalInput, api_base: str = "http://localhost:8000") -> dict:
    """Call the analyze API with snake_case to camelCase mapping."""
    import httpx

    payload = {
        "currentWealth": params.current_wealth,
        "targetWealth": params.target_wealth,
        "yearsToGoal": params.years_to_goal,
        "monthlyContribution": params.monthly_contribution,
        "riskProfile": params.risk_profile,
    }
    if params.monthly_income:
        payload["monthlyIncome"] = params.monthly_income

    response = httpx.post(f"{api_base}/api/analyze", json=payload)
    response.raise_for_status()
    return response.json()


def format_response(result: dict) -> str:
    """Format API response for chat context."""
    status_emoji = {"GREEN": "✅", "YELLOW": "⚠️", "RED": "🔴"}[result["status"]]
    prob = result["probabilityOfSuccess"]
    required = result["requiredMonthlyFor80Percent"]
    current_contrib = result["input"]["monthlyContribution"]

    output = f"""{status_emoji} **Goal Analysis: {result['status']}**

**Success Probability:** {prob:.0%}
**Your Monthly Savings:** ${current_contrib:,.0f}
**Required for 80% Success:** ${required:,.0f}

**Projected Outcomes:**
- Conservative (80% of outcomes beat this): ${result['projections']['percentile20']:,.0f}
- Median outcome: ${result['projections']['percentile50']:,.0f}
- Optimistic (top 20%): ${result['projections']['percentile80']:,.0f}

**Recommendations:**
"""
    for rec in result["recommendations"]:
        output += f"• {rec}\n"

    return output


async def execute_tool(params: dict) -> str:
    """
    Main entry point for MCP tool execution.

    Args:
        params: Parsed parameters from LLM

    Returns:
        Formatted string response for chat
    """
    try:
        # Validate with Pydantic
        validated = FinancialGoalInput(**params)

        # Call API
        result = call_api(validated)

        # Format for chat
        return format_response(result)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 422:
            errors = e.response.json().get("detail", [])
            error_msgs = [f"{err['loc'][-1]}: {err['msg']}" for err in errors]
            return f"Invalid input:\n" + "\n".join(f"• {msg}" for msg in error_msgs)
        return f"API error: {e.response.status_code}"
    except Exception as e:
        return f"Analysis failed: {str(e)}"
```

---

## Required Fields (LLM must extract or ask)

| Field | Required | Default | Extraction Hint |
|-------|----------|---------|-----------------|
| `current_wealth` | ✅ Yes | - | "I have $X saved/invested" |
| `target_wealth` | ✅ Yes | - | "I want $X" / expenses × 25 for FIRE |
| `years_to_goal` | ✅ Yes | - | Years given or calculated from ages |
| `monthly_contribution` | ✅ Yes | - | "$X/month" or annual ÷ 12 |
| `risk_profile` | No | moderate | Infer from context or default |
| `monthly_income` | No | null | Only if mentioned |

---

## Example Parsing

### Simple Case
**User:** "I have $50k saved, want $1M in 25 years, saving $800/month"

**Extracted:**
```json
{
  "current_wealth": 50000,
  "target_wealth": 1000000,
  "years_to_goal": 25,
  "monthly_contribution": 800,
  "risk_profile": "moderate"
}
```

### FIRE Case
**User:** "I spend $4000/month and want to retire early. Have $200k, save $2000/month, I'm 35."

**Extracted:**
```json
{
  "current_wealth": 200000,
  "target_wealth": 1200000,
  "years_to_goal": 20,
  "monthly_contribution": 2000,
  "risk_profile": "aggressive"
}
```

*Note: target = $4000 × 12 × 25 = $1.2M (4% rule)*

### Missing Info Case
**User:** "Can I retire with $2M?"

**Missing:** current_wealth, years_to_goal, monthly_contribution

**LLM should ask:** "To analyze this goal, I need to know:
1. How much do you have saved currently?
2. How many years until you want to retire?
3. How much can you save per month?"

---

## Response Format

```
✅ **Goal Analysis: GREEN**

**Success Probability:** 87%
**Your Monthly Savings:** $800
**Required for 80% Success:** $650

**Projected Outcomes:**
- Conservative (80% of outcomes beat this): $892,000
- Median outcome: $1,450,000
- Optimistic (top 20%): $2,100,000

**Recommendations:**
• Current plan is on track. Continue current savings rate.
• Consider reducing risk profile for similar outcomes with less volatility.
```

---

## Implementation Checklist

- [ ] Create `mcp_tool.py` with schema and executor
- [ ] Add `httpx` to requirements.txt (for async API calls)
- [ ] Test with sample natural language inputs
- [ ] Verify field name mapping (snake_case → camelCase)
- [ ] Test error handling (invalid years, negative values)
- [ ] Document MCP registration process

---

## Dependencies

Add to `requirements.txt`:
```
httpx>=0.27.0
```

---

## Architecture Decision

**Why LLM-based parsing (not server-side NLP):**
1. API stays deterministic and auditable
2. No LLM cost on backend
3. Works with any LLM (Claude, GPT-4, Llama, etc.)
4. MCP pattern is designed for this approach

**Reviewed by:** orchestrator agent (2026-01-17)
