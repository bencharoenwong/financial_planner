#!/usr/bin/env python3
"""
Financial Goal Feasibility Analyzer - CLI Tool
================================================
Chicago Global Capital - Parallax Planning Tool

Takes client financial goals as CSV input, analyzes feasibility using
deterministic market assumptions, and outputs recommendations with flags.

Usage:
    python financial_goal_analyzer.py input.csv output.csv
    python financial_goal_analyzer.py input.csv output.csv --config config.json
    python financial_goal_analyzer.py --sample sample_input.csv
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from core import RISK_PROFILES, FinancialAnalyzer, ThresholdConfig, AnalysisResult


# =============================================================================
# CSV I/O HANDLING
# =============================================================================


class CSVProcessor:
    """Handles CSV input/output for batch processing."""

    REQUIRED_COLUMNS = [
        "client_id",
        "current_wealth",
        "target_wealth",
        "years",
        "monthly_contribution",
    ]

    OPTIONAL_COLUMNS = {
        "risk_profile": "aggressive",
        "monthly_income": None,
    }

    def __init__(self, analyzer: FinancialAnalyzer):
        self.analyzer = analyzer

    def validate_input(self, df: pd.DataFrame) -> list:
        """Validate input DataFrame and return list of errors."""
        errors = []

        # Check required columns
        missing = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            errors.append(f"Missing required columns: {missing}")

        # Check data types and values
        if "current_wealth" in df.columns:
            if (df["current_wealth"] <= 0).any():
                errors.append("current_wealth must be positive")

        if "target_wealth" in df.columns:
            if (df["target_wealth"] <= 0).any():
                errors.append("target_wealth must be positive")

        if "years" in df.columns:
            if (df["years"] <= 0).any():
                errors.append("years must be positive")
            if (df["years"] > 100).any():
                errors.append("years exceeds reasonable maximum (100)")

        if "monthly_contribution" in df.columns:
            if (df["monthly_contribution"] < 0).any():
                errors.append("monthly_contribution cannot be negative")

        if "risk_profile" in df.columns:
            valid_profiles = set(RISK_PROFILES.keys())
            invalid = set(df["risk_profile"].str.lower().unique()) - valid_profiles
            if invalid:
                errors.append(
                    f"Invalid risk_profile values: {invalid}. Valid: {valid_profiles}"
                )

        return errors

    def process_file(self, input_path: str, output_path: str) -> dict:
        """
        Process input CSV and write results to output CSV.

        Returns summary statistics.
        """
        # Read input
        df = pd.read_csv(input_path)

        # Validate
        errors = self.validate_input(df)
        if errors:
            raise ValueError(f"Input validation failed:\n" + "\n".join(errors))

        # Fill defaults for optional columns
        for col, default in self.OPTIONAL_COLUMNS.items():
            if col not in df.columns:
                df[col] = default

        # Process each row
        results = []
        for _, row in df.iterrows():
            result = self.analyzer.analyze(
                client_id=str(row["client_id"]),
                current_wealth=float(row["current_wealth"]),
                target_wealth=float(row["target_wealth"]),
                years=int(row["years"]),
                monthly_contribution=float(row["monthly_contribution"]),
                risk_profile=str(row.get("risk_profile", "aggressive")),
                monthly_income=(
                    float(row["monthly_income"])
                    if pd.notna(row.get("monthly_income"))
                    else None
                ),
            )
            results.append(result)

        # Convert to DataFrame
        output_df = self._results_to_dataframe(results)

        # Write output
        output_df.to_csv(output_path, index=False)

        # Generate summary
        summary = {
            "total_records": len(results),
            "green_count": sum(1 for r in results if r.flag_status == "GREEN"),
            "yellow_count": sum(1 for r in results if r.flag_status == "YELLOW"),
            "red_count": sum(1 for r in results if r.flag_status == "RED"),
            "avg_success_prob": np.mean(
                [r.prob_success_with_contrib for r in results]
            ),
            "processed_at": datetime.now().isoformat(),
        }

        return summary

    def _results_to_dataframe(self, results: list[AnalysisResult]) -> pd.DataFrame:
        """Convert list of AnalysisResult to DataFrame."""
        records = []
        for r in results:
            records.append(
                {
                    # Input echo
                    "client_id": r.client_id,
                    "current_wealth": r.current_wealth,
                    "target_wealth": r.target_wealth,
                    "years": r.years,
                    "monthly_contribution": r.monthly_contribution,
                    "risk_profile": r.risk_profile,
                    "monthly_income": r.monthly_income,
                    # Market assumptions used
                    "assumed_return": r.arithmetic_return,
                    "assumed_volatility": r.volatility,
                    # Key outputs
                    "prob_success": r.prob_success_with_contrib,
                    "percentile_20": r.percentile_20_with_contrib,
                    "percentile_50_median": r.percentile_50_with_contrib,
                    "percentile_80": r.percentile_80_with_contrib,
                    "required_monthly_for_80pct": r.required_monthly_for_80pct,
                    "contribution_gap": r.required_monthly_for_80pct
                    - r.monthly_contribution,
                    # Lump sum only (for reference)
                    "prob_success_lump_only": r.prob_success_lump_only,
                    # Flags
                    "flag_status": r.flag_status,
                    "flag_reasons": "; ".join(r.flag_reasons) if r.flag_reasons else "",
                    # Recommendations
                    "recommendations": (
                        " | ".join(r.recommendations) if r.recommendations else ""
                    ),
                }
            )

        return pd.DataFrame(records)


# =============================================================================
# CLI INTERFACE
# =============================================================================


def create_sample_input(path: str):
    """Create a sample input CSV for testing."""
    sample_data = pd.DataFrame(
        [
            {
                "client_id": "CLIENT_001",
                "current_wealth": 10000,
                "target_wealth": 1000000,
                "years": 30,
                "monthly_contribution": 500,
                "risk_profile": "aggressive",
                "monthly_income": 8000,
            },
            {
                "client_id": "CLIENT_002",
                "current_wealth": 50000,
                "target_wealth": 500000,
                "years": 20,
                "monthly_contribution": 1000,
                "risk_profile": "moderate",
                "monthly_income": 10000,
            },
            {
                "client_id": "CLIENT_003",
                "current_wealth": 100000,
                "target_wealth": 2000000,
                "years": 25,
                "monthly_contribution": 2000,
                "risk_profile": "aggressive",
                "monthly_income": 15000,
            },
            {
                "client_id": "CLIENT_004",
                "current_wealth": 5000,
                "target_wealth": 100000,
                "years": 10,
                "monthly_contribution": 200,
                "risk_profile": "conservative",
                "monthly_income": 4000,
            },
            {
                "client_id": "CLIENT_005",
                "current_wealth": 250000,
                "target_wealth": 1000000,
                "years": 15,
                "monthly_contribution": 3000,
                "risk_profile": "moderate",
                "monthly_income": 20000,
            },
        ]
    )

    sample_data.to_csv(path, index=False)
    print(f"Sample input created: {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Financial Goal Feasibility Analyzer - Chicago Global Capital",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a CSV file
  python financial_goal_analyzer.py clients.csv results.csv

  # Generate sample input file
  python financial_goal_analyzer.py --sample sample_input.csv

  # Use custom thresholds
  python financial_goal_analyzer.py clients.csv results.csv --config thresholds.json

Required CSV columns:
  - client_id: Unique identifier
  - current_wealth: Starting capital ($)
  - target_wealth: Goal amount ($)
  - years: Time horizon
  - monthly_contribution: Planned monthly savings ($)

Optional CSV columns:
  - risk_profile: conservative, moderate, aggressive, very_aggressive (default: aggressive)
  - monthly_income: Monthly income for sustainability checks ($)
        """,
    )

    parser.add_argument("input", nargs="?", help="Input CSV file path")
    parser.add_argument("output", nargs="?", help="Output CSV file path")
    parser.add_argument("--config", help="JSON config file for custom thresholds")
    parser.add_argument(
        "--sample", metavar="PATH", help="Generate sample input CSV at PATH"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Print detailed output"
    )

    args = parser.parse_args()

    # Handle sample generation
    if args.sample:
        create_sample_input(args.sample)
        return 0

    # Validate required args for processing
    if not args.input or not args.output:
        parser.print_help()
        print("\nError: input and output paths required (or use --sample)")
        return 1

    # Load custom config if provided
    config = ThresholdConfig()
    if args.config:
        with open(args.config) as f:
            config_data = json.load(f)
            config = ThresholdConfig(**config_data)

    # Initialize analyzer and processor
    analyzer = FinancialAnalyzer(config=config, seed=args.seed)
    processor = CSVProcessor(analyzer)

    # Process file
    try:
        print(f"Processing: {args.input}")
        summary = processor.process_file(args.input, args.output)

        print(f"\n{'='*60}")
        print("PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"Output written to: {args.output}")
        print(f"\nSummary:")
        print(f"  Total records:    {summary['total_records']}")
        print(f"  GREEN (on track): {summary['green_count']}")
        print(f"  YELLOW (warning): {summary['yellow_count']}")
        print(f"  RED (critical):   {summary['red_count']}")
        print(f"  Avg success prob: {summary['avg_success_prob']:.1%}")
        print(f"  Processed at:     {summary['processed_at']}")

        if args.verbose:
            print(f"\nOutput preview:")
            output_df = pd.read_csv(args.output)
            print(
                output_df[
                    [
                        "client_id",
                        "prob_success",
                        "flag_status",
                        "required_monthly_for_80pct",
                    ]
                ].to_string()
            )

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
