"""
Financial Goal Analyzer - Core Module
=====================================
Shared calculation engine, models, and configuration.
"""

from core.config import RISK_PROFILES, THRESHOLDS, ThresholdConfig
from core.models import AnalysisResult, MarketAssumptions
from core.engine import FinancialAnalyzer

__all__ = [
    "RISK_PROFILES",
    "THRESHOLDS",
    "ThresholdConfig",
    "AnalysisResult",
    "MarketAssumptions",
    "FinancialAnalyzer",
]
