"""
Financial Goal Analyzer - FastAPI Backend
==========================================
Ready-to-deploy API for financial goal feasibility analysis.

Run locally:
    pip install -r requirements.txt
    uvicorn api:app --reload

Deploy to Vercel:
    - This file works as a Vercel serverless function
    - See vercel.json for configuration
"""

import io
import os
from datetime import datetime
from enum import Enum
from typing import Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field, field_validator

from core import RISK_PROFILES, FinancialAnalyzer

# =============================================================================
# APP SETUP
# =============================================================================

app = FastAPI(
    title="Financial Goal Analyzer API",
    description="Deterministic financial goal feasibility analysis",
    version="1.0.0",
)

# CORS configuration - restrict in production via environment variable
ALLOWED_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# MODELS
# =============================================================================


class RiskProfile(str, Enum):
    conservative = "conservative"
    moderate = "moderate"
    aggressive = "aggressive"
    very_aggressive = "very_aggressive"


class AnalyzeRequest(BaseModel):
    currentWealth: float = Field(..., gt=0, description="Starting capital ($)")
    targetWealth: float = Field(..., gt=0, description="Goal amount ($)")
    yearsToGoal: int = Field(..., ge=1, le=50, description="Time horizon (years)")
    monthlyContribution: float = Field(..., ge=0, description="Monthly savings ($)")
    riskProfile: RiskProfile = Field(default=RiskProfile.aggressive)
    monthlyIncome: Optional[float] = Field(
        default=None, ge=0, description="Monthly income for sustainability check"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "currentWealth": 10000,
                "targetWealth": 1000000,
                "yearsToGoal": 30,
                "monthlyContribution": 500,
                "riskProfile": "aggressive",
                "monthlyIncome": 8000,
            }
        }
    )

    @field_validator("targetWealth")
    @classmethod
    def target_greater_than_current(cls, v, info):
        # Allow target <= current (goal already achieved)
        return v


class Assumptions(BaseModel):
    arithmeticReturn: float
    geometricReturn: float
    volatility: float
    riskProfile: str


class Projections(BaseModel):
    percentile20: float
    percentile50: float
    percentile80: float


class LumpSumResults(BaseModel):
    probabilityOfSuccess: float
    percentile20: float
    percentile50: float
    percentile80: float


class AnalyzeResponse(BaseModel):
    input: dict
    assumptions: Assumptions
    probabilityOfSuccess: float
    requiredMonthlyFor80Percent: float
    contributionGap: float
    projections: Projections
    lumpSumOnly: LumpSumResults
    status: str
    flags: list[str]
    recommendations: list[str]
    analyzedAt: str
    version: str


class ProfileInfo(BaseModel):
    name: str
    arithmeticReturn: float
    volatility: float
    description: str


class BatchResult(BaseModel):
    total: int
    green: int
    yellow: int
    red: int
    results: list[AnalyzeResponse]


# =============================================================================
# ANALYZER INSTANCE
# =============================================================================

analyzer = FinancialAnalyzer()


# =============================================================================
# API ENDPOINTS
# =============================================================================


@app.get("/")
async def root():
    return {
        "name": "Financial Goal Analyzer API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": ["/api/analyze", "/api/analyze/batch", "/api/profiles", "/api/health"],
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/api/profiles", response_model=list[ProfileInfo])
async def get_profiles():
    """Get available risk profiles and their assumptions."""
    return [
        ProfileInfo(
            name=name, arithmeticReturn=arith, volatility=vol, description=desc
        )
        for name, (arith, vol, desc) in RISK_PROFILES.items()
    ]


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """
    Analyze a financial goal for feasibility.

    Returns probability of success, required contributions, and recommendations.
    """
    try:
        result = analyzer.analyze(
            client_id="api_request",
            current_wealth=request.currentWealth,
            target_wealth=request.targetWealth,
            years=request.yearsToGoal,
            monthly_contribution=request.monthlyContribution,
            risk_profile=request.riskProfile.value,
            monthly_income=request.monthlyIncome,
        )

        return AnalyzeResponse(
            input=request.model_dump(),
            assumptions=Assumptions(
                arithmeticReturn=result.arithmetic_return,
                geometricReturn=result.geometric_return,
                volatility=result.volatility,
                riskProfile=result.risk_profile,
            ),
            probabilityOfSuccess=round(result.prob_success_with_contrib, 4),
            requiredMonthlyFor80Percent=round(result.required_monthly_for_80pct, 2),
            contributionGap=round(
                result.required_monthly_for_80pct - result.monthly_contribution, 2
            ),
            projections=Projections(
                percentile20=round(result.percentile_20_with_contrib, 2),
                percentile50=round(result.percentile_50_with_contrib, 2),
                percentile80=round(result.percentile_80_with_contrib, 2),
            ),
            lumpSumOnly=LumpSumResults(
                probabilityOfSuccess=round(result.prob_success_lump_only, 4),
                percentile20=round(result.percentile_20_lump, 2),
                percentile50=round(result.percentile_50_lump, 2),
                percentile80=round(result.percentile_80_lump, 2),
            ),
            status=result.flag_status,
            flags=result.flag_reasons,
            recommendations=result.recommendations,
            analyzedAt=datetime.now().isoformat(),
            version="1.0.0",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/batch", response_model=BatchResult)
async def analyze_batch(file: UploadFile = File(...)):
    """
    Batch analyze multiple financial goals from a CSV file.

    CSV must have columns: client_id, current_wealth, target_wealth, years, monthly_contribution
    Optional columns: risk_profile, monthly_income

    Returns JSON array of analysis results.
    """
    # Validate file type
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # Validate required columns
        required = ["client_id", "current_wealth", "target_wealth", "years", "monthly_contribution"]
        missing = set(required) - set(df.columns)
        if missing:
            raise HTTPException(
                status_code=400, detail=f"Missing required columns: {missing}"
            )

        # Process each row
        results = []
        for _, row in df.iterrows():
            result = analyzer.analyze(
                client_id=str(row["client_id"]),
                current_wealth=float(row["current_wealth"]),
                target_wealth=float(row["target_wealth"]),
                years=int(row["years"]),
                monthly_contribution=float(row["monthly_contribution"]),
                risk_profile=str(row.get("risk_profile", "aggressive")).lower(),
                monthly_income=(
                    float(row["monthly_income"])
                    if pd.notna(row.get("monthly_income"))
                    else None
                ),
            )

            results.append(
                AnalyzeResponse(
                    input={
                        "client_id": result.client_id,
                        "currentWealth": result.current_wealth,
                        "targetWealth": result.target_wealth,
                        "yearsToGoal": result.years,
                        "monthlyContribution": result.monthly_contribution,
                        "riskProfile": result.risk_profile,
                        "monthlyIncome": result.monthly_income,
                    },
                    assumptions=Assumptions(
                        arithmeticReturn=result.arithmetic_return,
                        geometricReturn=result.geometric_return,
                        volatility=result.volatility,
                        riskProfile=result.risk_profile,
                    ),
                    probabilityOfSuccess=round(result.prob_success_with_contrib, 4),
                    requiredMonthlyFor80Percent=round(result.required_monthly_for_80pct, 2),
                    contributionGap=round(
                        result.required_monthly_for_80pct - result.monthly_contribution, 2
                    ),
                    projections=Projections(
                        percentile20=round(result.percentile_20_with_contrib, 2),
                        percentile50=round(result.percentile_50_with_contrib, 2),
                        percentile80=round(result.percentile_80_with_contrib, 2),
                    ),
                    lumpSumOnly=LumpSumResults(
                        probabilityOfSuccess=round(result.prob_success_lump_only, 4),
                        percentile20=round(result.percentile_20_lump, 2),
                        percentile50=round(result.percentile_50_lump, 2),
                        percentile80=round(result.percentile_80_lump, 2),
                    ),
                    status=result.flag_status,
                    flags=result.flag_reasons,
                    recommendations=result.recommendations,
                    analyzedAt=datetime.now().isoformat(),
                    version="1.0.0",
                )
            )

        # Summary stats
        green_count = sum(1 for r in results if r.status == "GREEN")
        yellow_count = sum(1 for r in results if r.status == "YELLOW")
        red_count = sum(1 for r in results if r.status == "RED")

        return BatchResult(
            total=len(results),
            green=green_count,
            yellow=yellow_count,
            red=red_count,
            results=results,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")


# =============================================================================
# VERCEL HANDLER
# =============================================================================

# For Vercel deployment, the app object is used directly
# No additional handler needed with FastAPI
