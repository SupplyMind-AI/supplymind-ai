---
document: Incident Report — Civil Unrest / Curfew, DC-LAX
document_id: INC-2024-031
incident_date: 2024-06-11
event_type: geopolitical
severity: 0.71
sites_affected: [DC-LAX]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Civil Unrest / Curfew, DC-LAX (INC-2024-031)

## Summary

On 11 June 2024, large-scale protests and a temporary overnight curfew in downtown Los Angeles caused rolling road closures affecting DC-LAX outbound routing for two days. SupplyMind flagged the event at severity 0.71 (Major). The mitigation was primarily about dispatch timing and zone avoidance rather than long-haul rerouting. Handled under `disruption_response_playbook.md` as a geopolitical / civil disruption.

## Timeline

| Date | Event |
|---|---|
| Jun 11, 14:00 | Protest and closure event ingested; downtown-adjacent routes flagged |
| Jun 11, 15:30 | Curfew announced (21:00–05:00); evening dispatch window at risk |
| Jun 11, 16:00 | Dispatch shifted earlier; affected zones mapped and avoided |
| Jun 12 | Early-morning dispatch used ahead of daytime closures |
| Jun 13 | Curfew lifted; normal routing resumes |

## Affected scope

- DC-LAX outbound routes passing through or near downtown closure zones.
- Approximately 380 shipments over two days required rescheduling or rerouting.
- No contractual same-day accounts breached.

## Root cause

Civil unrest and a government-imposed curfew caused unpredictable road closures. The constraint was time-of-day access to routes, not carrier capacity or long-haul availability.

## Mitigation

1. **Dispatch retiming** — moved evening dispatch earlier and used early-morning windows to clear volume before daytime closures.
2. **Zone avoidance** — mapped the affected closure zones and routed around them rather than reroute entire lanes.
3. **Curfew compliance** — held any dispatch that would place vehicles in the curfew window.
4. **Selective hold** — held non-urgent Standard Class for one day; prioritized time-critical volume.

## Impact

- DC-LAX outbound on-time held at 94.7% across the two days; no credits triggered.
- No force-majeure declaration; access was constrained by time of day but routes remained usable.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Add curfew-aware dispatch scheduling to the DC-LAX playbook | Logistics Operations Lead | 2024-07-20 |
| Maintain a downtown closure-zone map for civil-unrest scenarios | Logistics Operations | 2024-08-01 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `delay_escalation_policy.md` (POL-DEL-002)
- `warehouse_operations.md` (SOP-WH-005)
