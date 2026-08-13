---
document: Logistics Service Level Agreement
document_id: SLA-LOG-003
version: 3.0
owner: Commercial Operations
effective_date: 2026-07-01
review_cycle: Annual
classification: Internal — Contractual reference
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Logistics Service Level Agreement

## 1. Purpose

This SLA states the delivery and responsiveness commitments Meridian Logistics makes to its enterprise customers, and the remedies that apply when a commitment is missed.

## 2. Definitions

- **On-time delivery** — arrival within the committed transit window for the service level (`shipping_policy.md`).
- **On-time rate** — the share of a customer's deliveries that are on time, measured over a rolling 30-day window.
- **Response time** — elapsed business hours from a SupplyMind risk flag to the required review, per `delay_escalation_policy.md`.
- **Billing period** — one calendar month.

## 3. Account tiers and on-time targets

| Account tier | Contractual on-time rate | Internal operating target |
|---|---|---|
| Platinum | ≥ 97% | ≥ 98% |
| Gold | ≥ 95% | ≥ 97% |
| Silver | ≥ 93% | ≥ 95% |

Tiers are assigned commercially by contract value and volume; the applicable tier is recorded on the customer account.

## 4. Response-time commitments

Response commitments mirror the risk tiers in `delay_escalation_policy.md`.

| Risk tier | Acknowledgement | Action |
|---|---|---|
| Elevated | 8 business hours | Analyst review and mitigation plan |
| High | 4 business hours | Lead review; customer notification if window is threatened |
| High + active disruption | 2 business hours | Regional Manager review and routing decision |
| Contractual breach imminent | 1 hour | Head of Supply Chain engaged |

## 5. Delay credits

Where a customer's contractual on-time rate is missed in a billing period, service credits apply against that period's logistics charges for that account:

| On-time rate vs contractual target | Service credit |
|---|---|
| 2.0–4.9 points below target | 2% |
| 5.0–7.9 points below target | 5% |
| 8.0 or more points below target | 10% |

Credits are capped at 10% of the monthly logistics charge for the account and do not stack with credits for the same shipments under other agreements. Credits are calculated from SupplyMind's shipment-level records, not manual estimates.

## 6. Reporting

| Report | Cadence | Contents |
|---|---|---|
| Account performance summary | Monthly | On-time rate vs target, delayed-shipment count, credits due |
| At-risk exception report | Weekly | Elevated/High shipments, actions taken, open escalations |
| Disruption impact note | Per major event | Shipments affected, on-time impact, force-majeure claims |

## 7. Dispute process

A customer may dispute a monthly result within 15 business days of the report. Disputes are resolved against shipment-level prediction and delivery records. If a delivery record is found incorrect, the on-time rate and any credit are recalculated for that period.

## 8. Exclusions

Force majeure events — declared natural disasters, government action, or carrier-wide failures outside Meridian's control — are excluded from the on-time calculation for the affected shipments, provided the disruption is logged under `disruption_response_playbook.md` with its source and severity, and referenced by the relevant incident report.

## Related documents

- `shipping_policy.md` — committed transit windows
- `delay_escalation_policy.md` — risk tiers and escalation
- `disruption_response_playbook.md` — force-majeure logging

## Revision history

| Version | Date | Change |
|---|---|---|
| 3.0 | 2026-07-01 | Added Platinum/Gold/Silver account tiers and dispute process |
| 2.1 | 2026-02-10 | Revised credit schedule to point-based bands |
| 1.0 | 2025-05-01 | Initial issue |
