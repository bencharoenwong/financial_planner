"""
Financial Goal Analyzer - Core Calculation Engine

This module contains the Monte Carlo simulation engine for analyzing
financial goal feasibility.
"""

from typing import Optional

import numpy as np
from scipy import stats

from core.config import THRESHOLDS, ThresholdConfig
from core.models import AnalysisResult, MarketAssumptions


class FinancialAnalyzer:
    """Analyzes financial goals using Monte Carlo simulation."""

    def __init__(self, config: Optional[ThresholdConfig] = None, seed: int = 42):
        """
        Initialize the analyzer.

        Args:
            config: Optional custom threshold configuration
            seed: Random seed for reproducibility
        """
        self.config = config or ThresholdConfig()
        self.seed = seed
        np.random.seed(seed)

    def _calculate_lump_sum_distribution(
        self,
        initial: float,
        years: int,
        geo_return: float,
        volatility: float,
    ) -> tuple[float, float, float]:
        """
        Calculate wealth distribution for lump sum investment.

        Uses log-normal distribution for terminal wealth.

        Args:
            initial: Starting capital
            years: Time horizon
            geo_return: Geometric return
            volatility: Annual volatility

        Returns:
            Tuple of (p20, p50, p80) percentiles
        """
        mean_log = np.log(initial) + years * geo_return
        std_log = volatility * np.sqrt(years)

        z_20 = stats.norm.ppf(0.20)
        z_80 = stats.norm.ppf(0.80)

        p20 = np.exp(mean_log + z_20 * std_log)
        p50 = np.exp(mean_log)  # Median
        p80 = np.exp(mean_log + z_80 * std_log)

        return p20, p50, p80

    def _calculate_prob_success(
        self,
        initial: float,
        target: float,
        years: int,
        geo_return: float,
        volatility: float,
    ) -> float:
        """
        Calculate probability of reaching target with lump sum.

        Args:
            initial: Starting capital
            target: Target wealth
            years: Time horizon
            geo_return: Geometric return
            volatility: Annual volatility

        Returns:
            Probability of success (0-1)
        """
        mean_log = np.log(initial) + years * geo_return
        std_log = volatility * np.sqrt(years)

        z_target = (np.log(target) - mean_log) / std_log
        return 1 - stats.norm.cdf(z_target)

    def _simulate_with_contributions(
        self,
        initial: float,
        target: float,
        years: int,
        monthly_contribution: float,
        arith_return: float,
        volatility: float,
        n_simulations: int = 15000,
    ) -> tuple[float, float, float, float]:
        """
        Monte Carlo simulation with monthly contributions.

        Args:
            initial: Starting capital
            target: Target wealth
            years: Time horizon
            monthly_contribution: Monthly savings amount
            arith_return: Arithmetic return
            volatility: Annual volatility
            n_simulations: Number of simulation paths

        Returns:
            Tuple of (prob_success, p20, p50, p80)
        """
        monthly_return = arith_return / 12
        monthly_vol = volatility / np.sqrt(12)
        months = years * 12

        # Reset seed for reproducibility
        np.random.seed(self.seed)

        # Generate random returns
        returns = np.random.normal(monthly_return, monthly_vol, (n_simulations, months))

        # Calculate wealth paths
        wealth = np.full(n_simulations, initial, dtype=np.float64)

        for t in range(months):
            wealth = (wealth + monthly_contribution) * (1 + returns[:, t])

        prob_success = np.mean(wealth >= target)
        p20, p50, p80 = np.percentile(wealth, [20, 50, 80])

        return prob_success, p20, p50, p80

    def _find_required_monthly(
        self,
        initial: float,
        target: float,
        years: int,
        arith_return: float,
        volatility: float,
        target_prob: float = 0.80,
    ) -> float:
        """
        Binary search for required monthly contribution to hit target probability.

        Args:
            initial: Starting capital
            target: Target wealth
            years: Time horizon
            arith_return: Arithmetic return
            volatility: Annual volatility
            target_prob: Target success probability (default 80%)

        Returns:
            Required monthly contribution amount
        """
        low, high = 0.0, target / (years * 12)

        for _ in range(15):  # Binary search iterations
            mid = (low + high) / 2
            prob, _, _, _ = self._simulate_with_contributions(
                initial, target, years, mid, arith_return, volatility,
                n_simulations=5000  # Fewer sims for speed
            )

            if prob < target_prob:
                low = mid
            else:
                high = mid

        return (low + high) / 2

    def _determine_flags(
        self,
        prob_success: float,
        required_monthly: float,
        monthly_income: Optional[float],
        required_return: float,
    ) -> tuple[str, list]:
        """
        Determine flag status and reasons.

        Args:
            prob_success: Probability of success with current plan
            required_monthly: Required monthly contribution for 80% success
            monthly_income: Optional monthly income for sustainability check
            required_return: Required CAGR to reach target

        Returns:
            Tuple of (status, list of flag reasons)
        """
        flags = []
        status = "GREEN"

        # Check success probability
        if prob_success < self.config.success_prob_yellow:
            status = "RED"
            flags.append(f"Success probability {prob_success:.0%} critically low")
        elif prob_success < self.config.success_prob_green:
            status = "YELLOW"
            flags.append(f"Success probability {prob_success:.0%} below 80% threshold")

        # Check contribution burden
        if monthly_income and monthly_income > 0:
            contrib_pct = required_monthly / monthly_income
            if contrib_pct > self.config.contribution_critical_pct:
                status = "RED"
                flags.append(f"Required savings {contrib_pct:.0%} of income is unsustainable")
            elif contrib_pct > self.config.contribution_warning_pct:
                if status != "RED":
                    status = "YELLOW"
                flags.append(f"Required savings {contrib_pct:.0%} of income is high")

        # Check required return
        if required_return > self.config.required_return_critical:
            status = "RED"
            flags.append(f"Required return {required_return:.0%} exceeds realistic expectations")
        elif required_return > self.config.required_return_warning:
            if status != "RED":
                status = "YELLOW"
            flags.append(f"Required return {required_return:.0%} is aggressive")

        return status, flags

    def _generate_recommendations(self, result: AnalysisResult) -> list:
        """
        Generate actionable recommendations based on analysis.

        Args:
            result: The analysis result to generate recommendations for

        Returns:
            List of recommendation strings
        """
        recs = []

        if result.flag_status == "GREEN":
            recs.append("Current plan is on track. Continue current savings rate.")
            if result.prob_success_with_contrib > 0.90:
                recs.append("Consider reducing risk profile for similar outcomes with less volatility.")

        elif result.flag_status == "YELLOW":
            gap = result.required_monthly_for_80pct - result.monthly_contribution
            if gap > 0:
                recs.append(f"Increase monthly contribution by ${gap:,.0f} to reach 80% success probability.")

            if result.monthly_income:
                max_sustainable = result.monthly_income * self.config.contribution_warning_pct
                if result.required_monthly_for_80pct > max_sustainable:
                    recs.append("Alternative: Reduce target or extend timeline.")

            recs.append("Review risk profile - higher allocation may help but increases volatility.")

        else:  # RED
            recs.append("CRITICAL: Current goal is not achievable with stated parameters.")
            recs.append(f"Realistic target at 80% confidence: ${result.percentile_20_with_contrib:,.0f}")

            if result.years < 40:
                recs.append(f"Consider extending timeline beyond {result.years} years if possible.")

            if result.monthly_income:
                sustainable = result.monthly_income * self.config.contribution_warning_pct
                recs.append(f"Sustainable monthly savings at your income: ${sustainable:,.0f}")

        return recs

    def analyze(
        self,
        client_id: str,
        current_wealth: float,
        target_wealth: float,
        years: int,
        monthly_contribution: float,
        risk_profile: str = "aggressive",
        monthly_income: Optional[float] = None,
    ) -> AnalysisResult:
        """
        Analyze a single financial goal.

        Args:
            client_id: Unique identifier for the client/goal
            current_wealth: Starting capital
            target_wealth: Goal amount
            years: Time horizon
            monthly_contribution: Planned monthly savings
            risk_profile: One of conservative, moderate, aggressive, very_aggressive
            monthly_income: Optional monthly income for sustainability checks

        Returns:
            AnalysisResult with all calculations and recommendations
        """
        # Get market assumptions
        arith_return, volatility = MarketAssumptions.get_profile(risk_profile)
        geo_return = MarketAssumptions.geometric_return(arith_return, volatility)

        # Deterministic required return
        required_cagr = (target_wealth / current_wealth) ** (1 / years) - 1

        # Lump sum analysis
        p20_lump, p50_lump, p80_lump = self._calculate_lump_sum_distribution(
            current_wealth, years, geo_return, volatility
        )
        prob_lump = self._calculate_prob_success(
            current_wealth, target_wealth, years, geo_return, volatility
        )

        # With contributions analysis
        prob_contrib, p20_contrib, p50_contrib, p80_contrib = self._simulate_with_contributions(
            current_wealth, target_wealth, years, monthly_contribution,
            arith_return, volatility
        )

        # Find required monthly for 80% success
        required_monthly = self._find_required_monthly(
            current_wealth, target_wealth, years, arith_return, volatility
        )

        # Determine flags
        flag_status, flag_reasons = self._determine_flags(
            prob_contrib, required_monthly, monthly_income, required_cagr
        )

        # Build result
        result = AnalysisResult(
            client_id=client_id,
            current_wealth=current_wealth,
            target_wealth=target_wealth,
            years=years,
            monthly_contribution=monthly_contribution,
            risk_profile=risk_profile,
            monthly_income=monthly_income,
            required_cagr_deterministic=required_cagr,
            arithmetic_return=arith_return,
            geometric_return=geo_return,
            volatility=volatility,
            prob_success_lump_only=prob_lump,
            percentile_20_lump=p20_lump,
            percentile_50_lump=p50_lump,
            percentile_80_lump=p80_lump,
            prob_success_with_contrib=prob_contrib,
            percentile_20_with_contrib=p20_contrib,
            percentile_50_with_contrib=p50_contrib,
            percentile_80_with_contrib=p80_contrib,
            required_monthly_for_80pct=required_monthly,
            flag_status=flag_status,
            flag_reasons=flag_reasons,
        )

        # Generate recommendations
        result.recommendations = self._generate_recommendations(result)

        return result
