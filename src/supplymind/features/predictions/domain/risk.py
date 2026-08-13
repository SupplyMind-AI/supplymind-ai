"""Stable prediction decision and risk-band semantics."""
from __future__ import annotations


def risk_level_for_probability(probability: float, threshold: float) -> str:
    """Return a business-facing risk band aligned with the champion threshold.

    The classifier decision and UI risk band must not contradict each other.
    A score below the champion threshold is low risk; scores just above it are
    medium; materially higher scores are high.
    """
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")
    if probability < threshold:
        return "low"
    if probability < min(threshold + 0.20, 1.0):
        return "medium"
    return "high"


def decision_explanation(probability: float, threshold: float) -> str:
    if probability >= threshold:
        return (
            f"The model score ({probability:.1%}) is above the champion decision "
            f"threshold ({threshold:.1%}), so SupplyMind flags this shipment as delayed."
        )
    return (
        f"The model score ({probability:.1%}) is below the champion decision "
        f"threshold ({threshold:.1%}), so SupplyMind does not flag this shipment as delayed."
    )
