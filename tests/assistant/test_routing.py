from supplymind.features.assistant.application.routing import route_query
def test_combined():assert route_query('Why is this shipment delayed?',shipment_external_id='O1')=='combined'
def test_weather():assert route_query('What is the weather?',location='Berlin')=='weather'
def test_events():assert route_query('Any port strikes?')=='events'
def test_knowledge():assert route_query('What does the policy say?')=='knowledge'
