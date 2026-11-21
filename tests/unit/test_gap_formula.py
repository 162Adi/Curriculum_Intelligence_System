"""
Unit tests for the deterministic mathematical gap score calculation:
Gap Score = Importance * (1 - Coverage)
"""
import pytest
from app.agents.gap_analysis import GapAnalysisAgent


def test_gap_score_formula_calculation():
    """Verify that gap formula strictly calculates Importance * (1 - Coverage)."""
    # 1. High importance (90), zero coverage (0.0) -> Gap = 90 * 1.0 = 90.0 (CRITICAL)
    gap1 = GapAnalysisAgent.calculate_gap_metric(importance=90.0, coverage=0.0)
    assert gap1["score"] == 90.0
    assert gap1["severity"] == "CRITICAL"

    # 2. High importance (80), low coverage (0.25) -> Gap = 80 * 0.75 = 60.0 (HIGH)
    gap2 = GapAnalysisAgent.calculate_gap_metric(importance=80.0, coverage=0.25)
    assert gap2["score"] == 60.0
    assert gap2["severity"] == "HIGH"

    # 3. Medium importance (50), moderate coverage (0.4) -> Gap = 50 * 0.6 = 30.0 (MEDIUM)
    gap3 = GapAnalysisAgent.calculate_gap_metric(importance=50.0, coverage=0.4)
    assert gap3["score"] == 30.0
    assert gap3["severity"] == "MEDIUM"

    # 4. Low importance (40), high coverage (0.8) -> Gap = 40 * 0.2 = 8.0 (LOW)
    gap4 = GapAnalysisAgent.calculate_gap_metric(importance=40.0, coverage=0.8)
    assert gap4["score"] == 8.0
    assert gap4["severity"] == "LOW"

    # 5. Perfect coverage (1.0) -> Gap = 0.0 (LOW)
    gap5 = GapAnalysisAgent.calculate_gap_metric(importance=100.0, coverage=1.0)
    assert gap5["score"] == 0.0
    assert gap5["severity"] == "LOW"


def test_gap_boundary_values():
    """Verify edge boundaries: 0 importance, clamps, and floating coverage values."""
    zero_imp = GapAnalysisAgent.calculate_gap_metric(importance=0.0, coverage=0.5)
    assert zero_imp["score"] == 0.0
    assert zero_imp["severity"] == "LOW"

    # Importance 70, coverage 0.0 -> Gap = 70.0 -> exactly CRITICAL threshold
    crit_edge = GapAnalysisAgent.calculate_gap_metric(importance=70.0, coverage=0.0)
    assert crit_edge["score"] == 70.0
    assert crit_edge["severity"] == "CRITICAL"
