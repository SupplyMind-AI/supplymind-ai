---
document: Disruption Response Playbook
document_id: PLB-DIS-006
version: 1.1
owner: Logistics Operations
effective_date: 2026-06-01
review_cycle: Annual
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Disruption Response Playbook

## 1. Purpose

This playbook defines how Meridian Logistics responds to external disruptions that threaten shipments in transit or pending dispatch. It connects the disruption events surfaced by SupplyMind to concrete operational action.

## 2. Disruption types and typical response

Each external event carries a severity score from 0.0 to 1.0.

| Event type | First-line response |
|---|---|
| Severe weather | Check route weather for destination and hubs; prepare reroute around the affected node |
| Strike / labor action | Divert to secondary carrier; confirm surge capacity |
| Port congestion | Expedite priority containers; assess inbound supplier impact |
| Flooding | Reroute road segments; hold hazardous goods |
| Geopolitical disruption / armed conflict | Review affected lanes; shift mode or sourcing region; confirm customs and airspace status |
| Border closure | Hold or reroute cross-border shipments; notify affected accounts |
| Factory incident | Trigger supplier contingency (`supplier_risk_policy.md`) |
| Public health event | Cross-site load balancing; temporary staffing; prioritize contractual volume |
| Planned public event (sports, concert, festival, marathon) | Proactive: pre-position, adjust cut-offs, reroute around the affected corridor |
| Infrastructure / construction closure | Reroute with adjusted transit windows for the closure period; update lane configuration |
| Major transport interruption | Re-sequence dispatch; prioritize contractual commitments |

**Planned versus reactive events.** Planned public events and scheduled construction are known in advance and handled proactively regardless of severity band — pre-positioning and rerouting happen before the event, so the aim is zero window breaches rather than recovery.

**Carrier operational events.** Single-driver illness, vehicle breakdown, and similar carrier capacity issues are not external GDELT events. The carrier resolves them (driver reassignment, backup vehicle); Meridian monitors the affected shipments and escalates only if a committed window is threatened.

## 3. Severity bands

| Band | Severity | Meaning |
|---|---|---|
| Minor | `< 0.40` | Monitor; no routing change unless combined with high delay risk |
| Moderate | `0.40 – 0.69` | Review affected shipments; prepare alternative routing |
| Major | `≥ 0.70` | Act now; reroute or hold affected shipments and notify customers |

## 4. Detection

Disruption events are ingested from GDELT and route weather from Open-Meteo, matched to shipments by SupplyMind. An event is relevant to a shipment when its country matches the shipment origin or destination, its region matches a known route node, or its coordinates fall within the configured route radius.

## 5. Response decision matrix

Action combines event severity with the number and value of affected shipments.

| Event severity | Few / low-value shipments | Many / high-value shipments |
|---|---|---|
| Minor | Monitor | Review; hold rerouting in reserve |
| Moderate | Review; prepare alternates | Reroute proactively; notify affected customers |
| Major | Reroute or hold; notify | Reroute or hold; escalate to Regional Logistics Manager |

## 6. Combined with delay risk

A shipment that is high delay risk (`p ≥ 0.70`) **and** exposed to an active disruption follows the combined-risk rule in `delay_escalation_policy.md`: escalate to the Regional Logistics Manager within 2 business hours. Severity and delay risk are considered together — a Moderate event on an already high-risk shipment warrants the same urgency as a Major event.

## 7. Rerouting guidance

1. Prefer an alternate route that avoids the affected node while keeping the committed transit window.
2. Where the window cannot be held, choose the option that minimizes the breach and record the decision against the shipment.
3. For temperature-controlled or hazardous goods, never select a reroute that exceeds the product's stability window; hold instead and consult Warehouse Operations.

## 8. Responsibilities (RACI)

| Activity | Analyst | Lead | Regional Manager | Head of Supply Chain |
|---|---|---|---|---|
| Confirm affected shipments | R | A | I | — |
| Approve reroute (Moderate) | C | R/A | I | — |
| Approve reroute / hold (Major) | I | C | R/A | I |
| Declare force majeure | — | I | C | R/A |

## 9. Force majeure

A force-majeure declaration for the affected shipments requires: the event source and severity, the shipments affected, and Head of Supply Chain sign-off. Declared events are logged with a matching incident report and referenced in `logistics_sla.md` so the affected shipments are excluded from on-time calculations.

## 10. Communication and review

Customers with affected contractual commitments are notified within the response SLA for the shipment's risk tier. After a Major event closes, Logistics Operations produces an incident report (see the `incident_report_*` files) recording the event, its severity, the shipments affected, the on-time impact, and follow-up actions with owners and due dates.

## 11. Performance measures

| KPI | Target |
|---|---|
| Major events with a response within the tier SLA | 100% |
| Affected high-risk shipments rerouted or held before the affected node | ≥ 90% |
| Incident report published within 3 business days of event close | 100% |

## Related documents

- `delay_escalation_policy.md` — combined-risk escalation
- `logistics_sla.md` — force-majeure exclusion
- `warehouse_operations.md` — site-level response
- `supplier_risk_policy.md` — supplier contingency

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.1 | 2026-06-01 | Added per-event response table, RACI, and force-majeure process |
| 1.0 | 2025-07-01 | Initial issue |
