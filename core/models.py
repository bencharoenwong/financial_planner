"""
Data models for the Financial Goal Analyzer.
"""

from dataclasses import dataclass, field
from typing import Optional

from core.config import RISK_PROFILES


@dataclass
class MarketAssumptions:
    """Market return and volatility assumptions by risk profile."""

    @staticmethod
    def get_profile(name: str) -> tuple[float, float]:
        """
        Get (arithmetic_return, volatility) for a risk profile.

        Args:
            name: Risk profile name (conservative, moderate, aggressive, very_aggressive)

        Returns:
            Tuple of (arithmetic_return, volatility)
        """
        profile = RISK_PROFILES.get(name.lower())
        if profile:
            return profile[0], profile[1]
        # Default to moderate if unknown
        return RISK_PROFILES["moderate"][0], RISK_PROFILES["moderate"][1]

    @staticmethod
    def geometric_return(arithmetic: float, volatility: float) -> float:
        """Convert arithmetic to geometric return."""
        return arithmetic - (volatility ** 2) / 2


@dataclass
class AnalysisResult:
    """Results from analyzing a single financial goal."""

    # Input echo
    client_id: str
    current_wealth: float
    target_wealth: float
    years: int
    monthly_contribution: float
    risk_profile: str
    monthly_income: Optional[float]

    # Calculated values
    required_cagr_deterministic: float
    arithmetic_return: float
    geometric_return: float
    volatility: float

    # Probabilistic outcomes (lump sum only)
    prob_success_lump_only: float
    percentile_20_lump: float
    percentile_50_lump: float
    percentile_80_lump: float

    # With contributions
    prob_success_with_contrib: float
    percentile_20_with_contrib: float
    percentile_50_with_contrib: float
    percentile_80_with_contrib: float

    # Required monthly for 80% success
    required_monthly_for_80pct: float

    # Sustainable withdrawal income from target wealth (real annual income)
    # Based on safe withdrawal rates: conservative 3%, moderate 4%
    sustainable_income_conservative: float  # 3% SWR
    sustainable_income_moderate: float      # 4% SWR

    # Flags
    flag_status: str  # GREEN, YELLOW, RED
    flag_reasons: list = field(default_factory=list)

    # Recommendations
    recommendations: list = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "client_id": self.client_id,
            "current_wealth": self.current_wealth,
            "target_wealth": self.target_wealth,
            "years": self.years,
            "monthly_contribution": self.monthly_contribution,
            "risk_profile": self.risk_profile,
            "monthly_income": self.monthly_income,
            "required_cagr_deterministic": self.required_cagr_deterministic,
            "arithmetic_return": self.arithmetic_return,
            "geometric_return": self.geometric_return,
            "volatility": self.volatility,
            "prob_success_lump_only": self.prob_success_lump_only,
            "percentile_20_lump": self.percentile_20_lump,
            "percentile_50_lump": self.percentile_50_lump,
            "percentile_80_lump": self.percentile_80_lump,
            "prob_success_with_contrib": self.prob_success_with_contrib,
            "percentile_20_with_contrib": self.percentile_20_with_contrib,
            "percentile_50_with_contrib": self.percentile_50_with_contrib,
            "percentile_80_with_contrib": self.percentile_80_with_contrib,
            "required_monthly_for_80pct": self.required_monthly_for_80pct,
            "sustainable_income_conservative": self.sustainable_income_conservative,
            "sustainable_income_moderate": self.sustainable_income_moderate,
            "flag_status": self.flag_status,
            "flag_reasons": self.flag_reasons,
            "recommendations": self.recommendations,
        }
