# SupplyMind AI — Business Understanding

## Business problem

Supply-chain teams often learn about delays only after operational commitments
have already been affected. SupplyMind aims to identify shipment-delay risk
early enough for operations teams to investigate and intervene.
## V1 prediction objective

**Question:** Will this shipment be delayed?

**Output:** Binary prediction plus delay probability.

**Primary users:** logistics planners, operations managers, and supply-chain analysts.

**Primary actions:** investigate high-risk shipments, review weather and disruption
evidence, consult escalation policies, and choose mitigation actions.
## Prediction moment

Define the exact moment at which the model is expected to score a shipment.

Recommended V1 statement:

> The delay-risk prediction is generated after the shipment has been planned
> and route information is available, but before the actual delivery outcome
> or any post-delivery status is known.

Every model feature must be available at this moment.
## Target

- `1`: delayed
- `0`: not delayed

The exact target derivation must be confirmed from SynDelay documentation.
Columns used to derive the target must never be passed as model inputs.
## Success metrics

**Primary ML metrics**

- Recall for delayed shipments
- F1 score
- Precision
- ROC-AUC

Recall and F1 receive extra emphasis because missing a genuine delay is the
costly operational error.

**Business-facing success indicators**

- Share of delayed shipments identified before delivery
- Number of high-risk shipments surfaced for investigation
- Reduction in unanticipated operational exceptions

## Leakage checklist

Mark as unavailable if a field is created only after delivery:

- actual delivery timestamp
- actual transit duration
- final delivery status
- post-delivery exception code
- manually recorded delay reason
- any target-derived label

Dataset inspection must confirm the real SynDelay columns before training.