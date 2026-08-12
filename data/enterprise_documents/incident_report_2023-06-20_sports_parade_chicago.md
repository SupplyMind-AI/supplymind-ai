---
document: Incident Report — Championship Parade Road Closures, DC-CHI
document_id: INC-2023-038
incident_date: 2023-06-20
event_type: planned_public_event
severity: 0.42
sites_affected: [DC-CHI]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Championship Parade Road Closures, DC-CHI (INC-2023-038)

## Summary

On 20 June 2023, a downtown Chicago championship victory parade drew large crowds and closed several major roads for the day. Because the event was known five days in advance, it was handled proactively as a planned public event (severity 0.42, Moderate). The objective was zero window breaches rather than recovery. Handled under `disruption_response_playbook.md`, Section on planned versus reactive events.

## Timeline

| Date | Event |
|---|---|
| Jun 15 | Parade confirmed; event added to the DC-CHI operations calendar |
| Jun 18 | Affected corridors mapped; dispatch plan adjusted for Jun 20 |
| Jun 20, early AM | Priority volume pre-positioned and dispatched before closures |
| Jun 20, daytime | Remaining routes avoid the parade corridor |
| Jun 20, evening | Roads reopen; normal dispatch resumes |

## Affected scope

- DC-CHI outbound routes through downtown corridors for one day.
- Roughly 220 shipments re-sequenced or rerouted proactively.
- No contractual accounts at risk because mitigation was pre-planned.

## Root cause

A planned, publicized mass-attendance event with temporary road closures. Predictable and time-bounded, so the response was scheduling, not recovery.

## Mitigation

1. **Pre-positioning** — dispatched priority volume early in the morning before closures took effect.
2. **Corridor avoidance** — routed the day's remaining shipments around the parade corridor.
3. **Cut-off adjustment** — pulled the Same Day cut-off earlier for the affected day only, with customer notice.
4. **Calendar control** — logged the event so it was managed as routine rather than as an incident-in-progress.

## Impact

- DC-CHI on-time held at 97.2% for the day (no dip); no credits, no breaches.
- Demonstrated the value of an events calendar: a known event caused no service impact.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Maintain a rolling city-events calendar feed per site | Logistics Operations | 2023-07-31 |
| Add recurring major sports fixtures to the DC-CHI calendar | Site Lead | 2023-08-15 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `shipping_policy.md` (POL-SHP-001)
- `warehouse_operations.md` (SOP-WH-005)
