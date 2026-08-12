---
document: Incident Report — Carrier Strike, Northeast
document_id: INC-2026-057
incident_date: 2026-05-30
event_type: strike
severity: 0.88
sites_affected: [DC-NYC]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Carrier Strike, Northeast (INC-2026-057)

## Summary

On 30 May 2026, Keystone Express — the Northeast primary carrier — began a three-day labor strike. SupplyMind flagged the event at severity 0.88 (Major) and matched it to DC-NYC outbound volume. Diversion to the secondary carrier was capacity-constrained, and a portion of shipments breached their windows. Handled under `disruption_response_playbook.md` as a strike / labor action.

## Timeline

| Date | Event |
|---|---|
| May 30, 05:10 | Strike event ingested; DC-NYC outbound flagged Major |
| May 30, 06:30 | Escalated to Regional Logistics Manager |
| May 30, 08:00 | Diversion to Vanguard Freight begins; surge capacity limited |
| May 31 | High-risk shipments prioritized for available capacity |
| Jun 01 | ~210 shipments confirmed breached; customers notified |
| Jun 02 | Strike ends; Keystone Express resumes and clears backlog |

## Affected scope

- DC-NYC outbound First Class and Second Class to Northeast destinations.
- Roughly 210 shipments breached their committed window during the strike.
- 2 Gold accounts fell below their 95% contractual on-time rate for the billing period.

## Root cause

Carrier-wide labor dispute at the Northeast primary carrier. Secondary-carrier surge capacity was insufficient to fully absorb First/Second Class volume within the strike window — a single-carrier dependency for the region.

## Actions taken

1. Diverted recoverable volume to Vanguard Freight, prioritizing High-risk and contractual shipments.
2. Notified affected contractual accounts within the High-tier response SLA.
3. Applied service credits to the two Gold accounts that fell below target (10% band).

## Impact

- Northeast on-time rate fell to 89.4% for the period (Gold target 95%).
- 2 Gold accounts received a 10% service credit under `logistics_sla.md` (8+ points below target).
- Strike was not eligible for force majeure for breached shipments, as diversion capacity existed but was insufficient — recorded as a capacity gap, not an excludable event.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Negotiate guaranteed surge capacity in the Northeast secondary contract | Procurement | 2026-07-15 |
| Add a dual-carrier default for DC-NYC First/Second Class | Logistics Operations Lead | 2026-06-30 |
| Model strike scenarios in SupplyMind monitoring for the Northeast lane | Logistics Operations | 2026-08-01 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `logistics_sla.md` (SLA-LOG-003)
- `shipping_policy.md` (POL-SHP-001)
