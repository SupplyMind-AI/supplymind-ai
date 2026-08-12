---
document: Shipping Policy
document_id: POL-SHP-001
version: 2.1
owner: Logistics Operations
effective_date: 2026-06-01
review_cycle: Annual
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Shipping Policy

## 1. Purpose

This policy defines Meridian Logistics' standard shipping service levels, order cut-off times, and carrier allocation rules. It sets the baseline against which delivery performance and delay risk are measured across all four distribution centers.

## 2. Scope

Applies to all outbound customer shipments dispatched from Meridian distribution centers (DC-DAL, DC-CHI, DC-LAX, DC-NYC). It does not cover inbound supplier deliveries, which are governed by `supplier_risk_policy.md`.

## 3. Definitions

- **Transit window** — the committed number of business days from dispatch to delivery for a service level, excluding the dispatch day.
- **Cut-off** — the local distribution-center time by which an order must be received to dispatch the same business day.
- **Dispatch** — the moment a staged shipment leaves the dock and is handed to a carrier.
- **On time** — delivered within the transit window. **Delayed** — delivered after it.

## 4. Service levels and transit times

| Service level | Standard transit (business days) | Order cut-off (local DC time) | Typical use |
|---|---|---|---|
| Same Day | Same day | 10:00 | Critical, high-value, or contractual same-day accounts |
| First Class | 1–2 | 16:00 | Priority customer orders |
| Second Class | 2–4 | 15:00 | Standard priority |
| Standard Class | 4–7 | 14:00 | Default, cost-optimized |

Orders received after the cut-off are processed the next business day. Transit windows assume a valid, complete destination address (Section 8).

## 5. Carrier allocation

Carriers are allocated by service level, destination region, and rolling 30-day on-time performance.

| Region | Primary carrier | Secondary (surge / failover) |
|---|---|---|
| Central | Lone Star Logistics | Vanguard Freight |
| Midwest / Northeast | GreatLakes Transit | Vanguard Freight |
| West Coast | Cascade Carriers | Vanguard Freight |
| Northeast | Keystone Express | Vanguard Freight |

Allocation rules:

1. Same Day and First Class default to the regional primary carrier.
2. If a carrier's rolling 30-day on-time rate falls below 90%, new First Class volume is diverted to the secondary carrier until performance recovers for two consecutive weeks.
3. Standard Class is allocated to the lowest landed-cost carrier that still meets the transit window.
4. During an active disruption, allocation follows `disruption_response_playbook.md`, which may override cost-based allocation.

## 6. Incoterms

| Incoterm | Meridian responsibility ends at | Common use |
|---|---|---|
| DAP (Delivered At Place) | Named destination, duties unpaid | Default for domestic B2B |
| DDP (Delivered Duty Paid) | Named destination, duties paid | Contractual enterprise accounts |
| FCA (Free Carrier) | Handover to customer's carrier | Customer-managed transport |

## 7. Packaging and handling

Fragile, temperature-controlled, and hazardous goods follow the handling requirements in `warehouse_operations.md`. A temperature-controlled shipment must not be allocated to a service level whose transit window exceeds the product's stability window.

## 8. Address and data quality

Every shipment must carry a valid destination country, region, and postal code before dispatch. Incomplete address data is the most common avoidable cause of delay and prevents accurate route-weather and event matching in SupplyMind. Orders failing validation are held at the originating DC and flagged for correction, not dispatched.

## 9. Performance measures

| KPI | Target | Source |
|---|---|---|
| On-time delivery rate (rolling 30 days) | ≥ 97% internal | SupplyMind monitoring |
| Same-day dispatch compliance | ≥ 99% | Warehouse records |
| Address validation pass rate at order entry | ≥ 98% | Order management |

## 10. Exceptions

Deviations from committed service levels require Logistics Operations Lead approval and are recorded against the shipment. Systemic exceptions caused by external disruption are handled under `disruption_response_playbook.md`.

## Worked example

A Second Class order to Chicago is received at DC-DAL at 15:40 local. Because it arrives after the 15:00 cut-off, it is processed the next business day; its 2–4 day transit window starts from that next-day dispatch. If SupplyMind then scores it at `p = 0.71`, it is High risk and reviewed per `delay_escalation_policy.md`.

## Related documents

- `logistics_sla.md` — on-time targets and delay credits
- `delay_escalation_policy.md` — action when a shipment is at risk
- `warehouse_operations.md` — dispatch cut-offs and handling
- `disruption_response_playbook.md` — allocation under disruption

## Revision history

| Version | Date | Change |
|---|---|---|
| 2.1 | 2026-06-01 | Added incoterms and carrier failover thresholds |
| 2.0 | 2025-11-15 | Restructured service levels; added West Coast primary |
| 1.0 | 2025-03-01 | Initial issue |
