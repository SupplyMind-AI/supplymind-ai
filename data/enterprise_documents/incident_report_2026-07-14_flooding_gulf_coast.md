---
document: Incident Report — Gulf Coast Flooding
document_id: INC-2026-040
incident_date: 2026-07-14
event_type: flooding
severity: 0.79
sites_affected: [DC-DAL]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Gulf Coast Flooding (INC-2026-040)

## Summary

On 14 July 2026, tropical-storm rainfall caused flooding through the Houston corridor, disrupting road transport on DC-DAL southbound lanes. SupplyMind flagged the event at severity 0.79 (Major) and matched it to southbound outbound volume. The response was driven by the combined-risk rule: 96 affected shipments were already High delay risk, so the event was escalated even though volume was moderate. Handled under `disruption_response_playbook.md`.

## Timeline

| Date | Event |
|---|---|
| Jul 14, 05:45 | Flooding event ingested; DC-DAL southbound lanes flagged |
| Jul 14, 07:00 | 96 affected shipments identified, all High delay risk (`p ≥ 0.70`) |
| Jul 14, 07:40 | Combined-risk escalation to Regional Logistics Manager (within 2h) |
| Jul 14, 10:00 | Southbound volume rerouted north around the flooded corridor |
| Jul 15 | Hazardous-goods shipments held until corridor reopened |
| Jul 17 | Corridor reopened; held shipments dispatched |

## Affected scope

- 96 southbound outbound shipments from DC-DAL, all already High delay risk.
- 12 hazardous-goods shipments held rather than rerouted.
- 1 Platinum account with a contractual same-day commitment on the lane.

## Root cause

External flooding from tropical-storm rainfall; road corridor impassable. The affected shipments' pre-existing high delay risk amplified the impact, which is why a Moderate-volume event received a Major-tier response.

## Actions taken

1. Escalated to the Regional Logistics Manager under the combined-risk rule (`delay_escalation_policy.md`).
2. Rerouted 84 shipments north around the flooded corridor within their windows.
3. Held 12 hazardous-goods shipments per special-handling rules rather than accept an over-window reroute.
4. Notified the affected Platinum account within the 1-hour breach SLA.

## Impact

- Affected-lane on-time rate held at 93.6% through rerouting.
- 12 held hazardous-goods shipments logged as force majeure and excluded per `logistics_sla.md`.
- No service credit triggered for the Platinum account after force-majeure exclusion.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Pre-map flood-alternate routes for all Gulf Coast lanes | Logistics Operations Lead | 2026-09-01 |
| Add corridor-level flood watch to SupplyMind event matching | Logistics Operations | 2026-08-15 |
| Review hazardous-goods hold vs reroute thresholds | Warehouse Operations | 2026-08-30 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `delay_escalation_policy.md` (POL-DEL-002)
- `warehouse_operations.md` (SOP-WH-005)
