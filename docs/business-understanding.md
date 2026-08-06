1. Current Situation

Supply chain managers don't know early enough whether a shipment will be delayed.

Consequences:
• higher transportation cost
• poor customer satisfaction
• missed SLAs
• inventory shortages

2. Objective:
Predict: Will this shipment be delayed?

Output: Probability of delay

Business users:
- Logistics planners
- Operations managers
- Supply chain analysts

3. Success Metrics

- Business metrics
- Reduce unexpected delays
- Improve planning
- Improve resource allocation

4. ML metrics

- Recall
- Precision
- F1
- ROC AUC

4. When is the prediction made?

Shipment created

↓

Weather available

↓

Origin known

↓

Destination known

↓

Carrier known

↓

Predict delay

5. Target

Delayed = 1

Not Delayed = 0