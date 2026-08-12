---
document: Delay Escalation Policy
document_id: POL-DEL-002
version: 1.3
owner: Logistics Operations
effective_date: 2026-06-01
review_cycle: Annual
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Delay Escalation Policy

## 1. Purpose

This policy defines how shipments flagged with delay risk are triaged, who reviews them at each level, and when a shipment must be escalated. It applies to the delay-risk scores produced by SupplyMind's prediction model.

## 2. Definitions

- **Predicted delay probability (`p`)** — the model's estimated probability that a shipment is delayed.
- **Active external disruption** — a GDELT or weather event, matched to the shipment's route, with severity ≥ 0.40 (`disruption_response_playbook.md`).
- **Response SLA** — the elapsed business-hours time within which the owner must review a flagged shipment. The SLA clock runs during business hours only: 06:00–20:00 local, Monday–Saturday.

## 3. Risk tiers

| Tier | Predicted delay probability | Owner | Response SLA |
|---|---|---|---|
| Low | `p < 0.40` | Automated monitoring only | None; daily review |
| Elevated | `0.40 ≤ p < 0.70` | Logistics Operations Analyst | 8 business hours |
| High | `p ≥ 0.70` | Logistics Operations Lead | 4 business hours |

A shipment is **high risk** when its predicted delay probability exceeds 70%. High-risk shipments must be reviewed by the logistics operations team within the response SLA.

## 4. Escalation ladder

Escalation moves up one level when a review cannot resolve the risk within its SLA, or when the combined-risk rule (Section 6) applies.

```
Logistics Operations Analyst
        ↓
Logistics Operations Lead
        ↓
Regional Logistics Manager
        ↓
Head of Supply Chain
```

## 5. Responsibilities (RACI)

| Activity | Analyst | Lead | Regional Manager | Head of Supply Chain |
|---|---|---|---|---|
| Review Elevated shipment | R | A | I | — |
| Review High shipment | C | R/A | I | — |
| Combined-risk escalation | I | C | R/A | I |
| Contractual-breach decision | — | I | C | R/A |

R = responsible, A = accountable, C = consulted, I = informed.

## 6. Weather and combined risk

When severe weather affects the destination or a major transportation hub on the route, operations must review alternative routing before the shipment reaches the affected node. Route weather is provided by SupplyMind's weather tool.

A shipment that is **both** high risk (`p ≥ 0.70`) **and** exposed to an active external disruption must be escalated to the **Regional Logistics Manager within 2 business hours**. If it also carries a contractual same-day or First Class commitment at risk of breach, escalate to the Head of Supply Chain within 1 hour.

## 7. Required actions on review

Each review records, at minimum: shipment ID, tier at review, predicted probability, any matched disruption and its severity, the mitigation chosen (monitor, reroute, expedite, hold, notify), the owner, and a timestamp. Customer notification is required when a committed window is threatened for a contractual account.

## 8. Worked examples

- **Elevated, no disruption.** `p = 0.52`, clear route. Analyst reviews within 8 business hours, confirms carrier on schedule, marks *monitor*. No escalation.
- **High, no disruption.** `p = 0.74`, clear route. Lead reviews within 4 business hours, expedites to the secondary carrier to protect the window.
- **Combined risk.** `p = 0.82` with a Major storm (severity 0.81) on the destination hub. Escalated to the Regional Logistics Manager within 2 business hours; shipment rerouted per `disruption_response_playbook.md`.

## 9. Performance measures

| KPI | Target |
|---|---|
| High-risk shipments reviewed within SLA | ≥ 95% |
| Mean time to first review (High tier) | ≤ 2 business hours |
| Combined-risk escalations acknowledged within 2h | 100% |

## Related documents

- `logistics_sla.md` — response-time commitments and delay credits
- `disruption_response_playbook.md` — disruption severity and routing
- `shipping_policy.md` — service levels and commitments

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.3 | 2026-06-01 | Added RACI, SLA-clock definition, and worked examples |
| 1.2 | 2026-01-20 | Added combined-risk rule and 2-hour escalation |
| 1.0 | 2025-04-01 | Initial issue |
