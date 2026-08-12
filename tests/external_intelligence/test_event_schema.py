import pytest
from pydantic import ValidationError

from supplymind.features.external_intelligence.domain.schemas import (
    EventType,
    ExtractedSupplyChainEvent,
)


def test_event_type_is_controlled():
    event = ExtractedSupplyChainEvent(
        is_relevant=True,
        event_type=EventType.FLOODING,
        normalized_title="Severe flooding disrupts Shanghai transport",
        summary="Flooding caused major transport interruptions.",
        severity=0.8,
        country="China",
        region="Shanghai",
    )

    assert event.event_type == EventType.FLOODING


def test_invalid_event_type_is_rejected():
    with pytest.raises(ValidationError):
        ExtractedSupplyChainEvent(
            is_relevant=True,
            event_type="loan_for_shipbuilding",
            normalized_title="Invalid event type",
            severity=0.5,
        )
