from supplymind.features.assistant.application.routing import route_query

def test_combined_shipment_question():
    assert route_query("Why is this shipment at risk?",shipment_external_id="TEST-1")=="combined"

def test_policy_question_uses_knowledge():
    assert route_query("What does our policy say about escalation?")=="knowledge"
