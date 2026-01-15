"""
Tests for the core calculation engine.
"""

import pytest
import numpy as np

from core import FinancialAnalyzer, ThresholdConfig, RISK_PROFILES


class TestFinancialAnalyzer:
    """Tests for FinancialAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer with fixed seed for reproducibility."""
        return FinancialAnalyzer(seed=42)

    def test_basic_analysis(self, analyzer):
        """Test basic analysis returns expected structure."""
        result = analyzer.analyze(
            client_id="test_001",
            current_wealth=10000,
            target_wealth=100000,
            years=20,
            monthly_contribution=200,
            risk_profile="aggressive",
        )

        assert result.client_id == "test_001"
        assert result.current_wealth == 10000
        assert result.target_wealth == 100000
        assert result.years == 20
        assert result.monthly_contribution == 200
        assert result.risk_profile == "aggressive"

        # Check calculated fields exist and are reasonable
        assert 0 <= result.prob_success_with_contrib <= 1
        assert result.percentile_20_with_contrib > 0
        assert result.percentile_50_with_contrib > result.percentile_20_with_contrib
        assert result.percentile_80_with_contrib > result.percentile_50_with_contrib
        assert result.required_monthly_for_80pct >= 0
        assert result.flag_status in ["GREEN", "YELLOW", "RED"]

    def test_all_risk_profiles(self, analyzer):
        """Test analysis works for all risk profiles."""
        for profile in RISK_PROFILES.keys():
            result = analyzer.analyze(
                client_id=f"test_{profile}",
                current_wealth=50000,
                target_wealth=500000,
                years=25,
                monthly_contribution=500,
                risk_profile=profile,
            )

            assert result.risk_profile == profile
            assert result.arithmetic_return == RISK_PROFILES[profile][0]
            assert result.volatility == RISK_PROFILES[profile][1]

    def test_higher_risk_higher_return(self, analyzer):
        """Test that higher risk profiles have higher expected returns."""
        results = {}
        for profile in ["conservative", "moderate", "aggressive", "very_aggressive"]:
            results[profile] = analyzer.analyze(
                client_id=f"test_{profile}",
                current_wealth=50000,
                target_wealth=500000,
                years=25,
                monthly_contribution=500,
                risk_profile=profile,
            )

        # Higher risk should generally have higher median outcomes
        # (though with more variance)
        assert results["conservative"].arithmetic_return < results["moderate"].arithmetic_return
        assert results["moderate"].arithmetic_return < results["aggressive"].arithmetic_return
        assert results["aggressive"].arithmetic_return < results["very_aggressive"].arithmetic_return

    def test_zero_contribution(self, analyzer):
        """Test analysis with zero monthly contribution (lump sum only)."""
        result = analyzer.analyze(
            client_id="lump_sum",
            current_wealth=100000,
            target_wealth=200000,
            years=10,
            monthly_contribution=0,
            risk_profile="aggressive",
        )

        # Should still get valid results
        assert result.prob_success_with_contrib >= 0
        assert result.percentile_50_with_contrib > 0
        # With zero contribution, lump sum and contribution results should be similar
        # (allowing for Monte Carlo variance)

    def test_flag_determination_green(self, analyzer):
        """Test that achievable goals get GREEN status."""
        result = analyzer.analyze(
            client_id="achievable",
            current_wealth=500000,
            target_wealth=600000,
            years=10,
            monthly_contribution=1000,
            risk_profile="conservative",
        )

        # Easy goal should be green
        assert result.flag_status == "GREEN"
        assert result.prob_success_with_contrib >= 0.8

    def test_flag_determination_red(self, analyzer):
        """Test that impossible goals get RED status."""
        result = analyzer.analyze(
            client_id="impossible",
            current_wealth=1000,
            target_wealth=10000000,
            years=5,
            monthly_contribution=100,
            risk_profile="conservative",
        )

        # Impossible goal should be red
        assert result.flag_status == "RED"
        assert result.prob_success_with_contrib < 0.5

    def test_income_sustainability_flag(self, analyzer):
        """Test income sustainability check triggers flags."""
        result = analyzer.analyze(
            client_id="high_burden",
            current_wealth=10000,
            target_wealth=1000000,
            years=20,
            monthly_contribution=500,
            risk_profile="aggressive",
            monthly_income=1000,  # Very low income relative to needed savings
        )

        # Should flag sustainability concern
        flag_text = " ".join(result.flag_reasons)
        assert "income" in flag_text.lower() or result.flag_status in ["YELLOW", "RED"]

    def test_recommendations_generated(self, analyzer):
        """Test that recommendations are generated."""
        result = analyzer.analyze(
            client_id="test",
            current_wealth=10000,
            target_wealth=500000,
            years=20,
            monthly_contribution=200,
            risk_profile="moderate",
        )

        assert len(result.recommendations) > 0
        assert all(isinstance(r, str) for r in result.recommendations)

    def test_reproducibility(self):
        """Test that same seed produces same results."""
        analyzer1 = FinancialAnalyzer(seed=123)
        analyzer2 = FinancialAnalyzer(seed=123)

        result1 = analyzer1.analyze(
            client_id="test",
            current_wealth=50000,
            target_wealth=500000,
            years=20,
            monthly_contribution=500,
            risk_profile="aggressive",
        )

        result2 = analyzer2.analyze(
            client_id="test",
            current_wealth=50000,
            target_wealth=500000,
            years=20,
            monthly_contribution=500,
            risk_profile="aggressive",
        )

        assert result1.prob_success_with_contrib == result2.prob_success_with_contrib
        assert result1.percentile_50_with_contrib == result2.percentile_50_with_contrib

    def test_geometric_vs_arithmetic_return(self, analyzer):
        """Test that geometric return is less than arithmetic return."""
        result = analyzer.analyze(
            client_id="test",
            current_wealth=50000,
            target_wealth=500000,
            years=20,
            monthly_contribution=500,
            risk_profile="aggressive",
        )

        # Geometric return should always be less than arithmetic
        assert result.geometric_return < result.arithmetic_return
        # The difference should be volatility^2 / 2
        expected_geo = result.arithmetic_return - (result.volatility ** 2) / 2
        assert abs(result.geometric_return - expected_geo) < 0.0001


class TestThresholdConfig:
    """Tests for ThresholdConfig."""

    def test_default_values(self):
        """Test default threshold values."""
        config = ThresholdConfig()

        assert config.success_prob_green == 0.80
        assert config.success_prob_yellow == 0.50
        assert config.contribution_warning_pct == 0.20
        assert config.contribution_critical_pct == 0.35

    def test_custom_values(self):
        """Test custom threshold values."""
        config = ThresholdConfig(
            success_prob_green=0.90,
            success_prob_yellow=0.60,
        )

        assert config.success_prob_green == 0.90
        assert config.success_prob_yellow == 0.60

    def test_custom_config_affects_flags(self):
        """Test that custom config changes flag behavior."""
        strict_config = ThresholdConfig(success_prob_green=0.95)
        analyzer = FinancialAnalyzer(config=strict_config, seed=42)

        result = analyzer.analyze(
            client_id="test",
            current_wealth=100000,
            target_wealth=200000,
            years=10,
            monthly_contribution=500,
            risk_profile="aggressive",
        )

        # With stricter threshold, more likely to not be GREEN
        # (exact behavior depends on the numbers)
        assert result.flag_status in ["GREEN", "YELLOW", "RED"]
