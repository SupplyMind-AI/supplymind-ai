from supplymind.features.predictions.domain.risk import risk_level_for_probability, decision_explanation

def test_risk_band_never_calls_below_threshold_medium_or_high():
    assert risk_level_for_probability(.29,.30)=="low"
    assert risk_level_for_probability(.36,.30)=="medium"
    assert risk_level_for_probability(.55,.30)=="high"

def test_decision_explanation_is_threshold_grounded():
    text=decision_explanation(.36,.30)
    assert "above" in text and "36.0%" in text and "30.0%" in text
