---
document: Incident Report — Wildfire / Highway Closure, DC-LAX
document_id: INC-2023-069
incident_date: 2023-10-08
event_type: severe_weather
severity: 0.66
sites_affected: [DC-LAX]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Wildfire / Highway Closure, DC-LAX (INC-2023-069)

## Summary

On 8 October 2023, a wildfire closed a key interstate segment on a West Coast lane and degraded air quality around DC-LAX, reducing dock throughput. SupplyMind flagged the event at severity 0.66 (Moderate). The mitigation combined rerouting with a throughput and staff-safety response — a different profile from flooding or storms. Handled under `disruption_response_playbook.md` as severe weather / wildfire.

## Timeline

| Date | Event |
|---|---|
| Oct 08 | Wildfire and interstate closure ingested; affected lane flagged |
| Oct 08 | Air-quality advisory issued for the DC-LAX area |
| Oct 09 | Alternate interstate routing in use; dock throughput reduced |
| Oct 10 | PPE distributed; staggered dock work to limit exposure |
| Oct 12 | Fire contained; interstate reopens; routing normalizes |

## Affected scope

- One West Coast interstate lane closed; affected outbound rerouted.
- DC-LAX dock throughput reduced by air-quality-related work slowdowns.
- Approximately 300 shipments rerouted or re-sequenced.

## Root cause

Wildfire closed a road segment and degraded local air quality. Two distinct constraints — a routing constraint on one lane and a throughput/health constraint at the site.

## Mitigation

1. **Reroute** — moved the affected lane's volume to an alternate interstate keeping the transit window.
2. **Throughput management** — staged outbound at reduced dock throughput, prioritizing contractual and High-risk shipments.
3. **Staff safety** — distributed N95 protection and staggered dock work during poor air quality.
4. **Prioritization** — deferred non-urgent Standard Class until throughput recovered.

## Impact

- West Coast affected-lane on-time held at 95.1%; no credits triggered.
- No force-majeure declaration; both routing and throughput had workable mitigations.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Pre-map wildfire-season alternate routes for West Coast lanes | Logistics Operations Lead | 2023-12-01 |
| Keep an air-quality PPE stock at DC-LAX | Warehouse Operations | 2023-11-10 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `warehouse_operations.md` (SOP-WH-005)
- `delay_escalation_policy.md` (POL-DEL-002)
