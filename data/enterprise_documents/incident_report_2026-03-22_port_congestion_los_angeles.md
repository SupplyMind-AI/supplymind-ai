---
document: Incident Report — Port Congestion, LA/Long Beach
document_id: INC-2026-041
incident_date: 2026-03-22
event_type: port_congestion
severity: 0.72
sites_affected: [DC-LAX]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Port Congestion, LA/Long Beach (INC-2026-041)

## Summary

From 22 March 2026, vessel bunching and a dockside labor shortage caused sustained congestion at the Los Angeles / Long Beach port complex. SupplyMind flagged the event at severity 0.72 (Major) and matched it to inbound supplier containers destined for DC-LAX and to downstream West Coast outbound volume. Handled under `disruption_response_playbook.md` as port congestion.

## Timeline

| Date | Event |
|---|---|
| Mar 22 | Congestion event ingested; inbound DC-LAX containers flagged |
| Mar 23 | Two Tier-C suppliers temporarily reassessed to Tier D on delivery slippage |
| Mar 24 | Priority containers expedited; alternate supplier activated for one product line |
| Mar 27 | West Coast outbound proactively rerouted where windows were threatened |
| Apr 02 | Congestion eased; supplier tiers reverted after two on-time deliveries |

## Affected scope

- Inbound: 3 supplier container loads delayed 4–9 days at berth.
- Downstream: ~540 West Coast outbound shipments moved to Elevated risk due to component availability.
- 2 suppliers temporarily elevated to Tier D under `supplier_risk_policy.md`.

## Root cause

External port congestion (vessel bunching plus labor shortage) outside Meridian's control. Compounded by one single-source product line without an active alternate at the time of the event.

## Actions taken

1. Expedited priority inbound containers via drayage once released.
2. Activated the approved alternate supplier for the single-source line, restoring component flow.
3. Proactively rerouted threatened West Coast outbound shipments to protect committed windows.
4. Increased buffer stock targets at DC-LAX for affected SKUs.

## Impact

- West Coast outbound on-time rate held at 95.8% through proactive rerouting (no credit triggered).
- No force-majeure declaration required for outbound; inbound delays absorbed by buffer and expedite.
- Two suppliers spent 11 days in Tier D before reverting to Tier C.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Qualify a second source for the affected single-source line | Procurement | 2026-05-15 |
| Raise DC-LAX buffer stock for port-dependent SKUs | Warehouse Operations | 2026-04-20 |
| Add earlier inbound PO visibility to SupplyMind ingestion | Logistics Operations | 2026-06-01 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `supplier_risk_policy.md` (POL-SUP-004)
- `warehouse_operations.md` (SOP-WH-005)
