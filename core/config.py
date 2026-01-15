"""
Configuration constants for the Financial Goal Analyzer.

Risk profiles and thresholds are defined here as the single source of truth.
"""

from dataclasses import dataclass


# Risk profiles: (arithmetic_return, volatility, description)
RISK_PROFILES = {
    "conservative": (0.06, 0.10, "Bond-heavy allocation (70% bonds, 30% stocks)"),
    "moderate": (0.08, 0.13, "Balanced allocation (40% bonds, 60% stocks)"),
    "aggressive": (0.10, 0.16, "Equity-focused (S&P 500-like)"),
    "very_aggressive": (0.12, 0.20, "Concentrated/leveraged positions"),
}


# Flag thresholds
THRESHOLDS = {
    "success_prob_green": 0.80,      # >= 80% = on track
    "success_prob_yellow": 0.50,     # >= 50% = needs attention
    "contribution_warning_pct": 0.20,   # > 20% of income = warning
    "contribution_critical_pct": 0.35,  # > 35% of income = unsustainable
    "required_return_warning": 0.12,    # > 12% = aggressive
    "required_return_critical": 0.15,   # > 15% = unrealistic
}


@dataclass
class ThresholdConfig:
    """Configurable thresholds for flags and recommendations."""

    success_prob_green: float = 0.80
    success_prob_yellow: float = 0.50
    contribution_warning_pct: float = 0.20
    contribution_critical_pct: float = 0.35
    required_return_warning: float = 0.12
    required_return_critical: float = 0.15
    min_horizon_years: int = 1
    max_horizon_years: int = 50
