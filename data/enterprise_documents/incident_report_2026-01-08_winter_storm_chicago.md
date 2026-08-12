---
document: Incident Report — Winter Storm, DC-CHI
document_id: INC-2026-014
incident_date: 2026-01-08
event_type: severe_weather
severity: 0.84
sites_affected: [DC-CHI]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Winter Storm, DC-CHI (INC-2026-014)

## Summary

On 8 January 2026 a winter storm dropped roughly 14 inches of snow across the Chicago metro over 30 hours. GreatLakes Transit, the Midwest primary carrier, suspended line-haul operations for approximately 36 hours. SupplyMind flagged the event (severity 0.84, Major) and matched it to outbound volume from DC-CHI. The event was handled under `disruption_response_playbook.md` as a Major weather disruption.

## Timeline

| Time (local) | Event |
|---|---|
| Jan 8, 04:20 | SupplyMind ingests severe-weather event; DC-CHI outbound flagged |
| Jan 8, 06:00 | Logistics Operations Lead confirms 1,240 affected outbound shipments |
| Jan 8, 07:30 | GreatLakes Transit suspends line-haul; reroute planning begins |
| Jan 8, 09:00 | Escalated to Regional Logistics Manager (Major + high-risk volume) |
| Jan 8, 11:00 | ~610 shipments rerouted via DC-DAL to Vanguard Freight |
| Jan 9, 20:00 | GreatLakes Transit resumes; backlog dispatch begins |
| Jan 11 | On-time recovered to baseline for DC-CHI |

## Affected scope

- 1,240 outbound shipments (First Class and Second Class), primarily Midwest and Northeast destinations.
- 3 Gold accounts and 1 Platinum account with contractual commitments at risk.
- 74 temperature-controlled shipments held rather than rerouted, to stay within stability windows.

## Root cause

Regional carrier line-haul suspension caused by 14-inch snowfall and hazardous road conditions; no fault in Meridian handling. Address and prediction data were complete, so matching and rerouting were accurate.

## Actions taken

1. Rerouted ~610 recoverable shipments via DC-DAL to the secondary carrier (Vanguard Freight).
2. Held 74 temperature-controlled shipments per `warehouse_operations.md` special-handling rules.
3. Notified all affected contractual accounts within the High-tier response SLA.
4. Declared force majeure for 380 shipments that could not hold their window during the suspension.

## Impact

- DC-CHI rolling weekly on-time rate fell to 91.2% for affected accounts (baseline ≥ 97%).
- 380 shipments logged as force majeure and excluded from on-time calculation per `logistics_sla.md`.
- No service credits triggered, because force-majeure shipments were excluded and non-excluded volume stayed above tier thresholds.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Pre-position winter surge capacity with Vanguard Freight (Nov–Feb) | Regional Logistics Manager | 2026-11-01 |
| Add a standing cold-weather reroute plan DC-CHI → DC-DAL | Logistics Operations Lead | 2026-03-15 |
| Review GreatLakes Transit winter continuity commitments | Procurement | 2026-04-01 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `delay_escalation_policy.md` (POL-DEL-002)
- `logistics_sla.md` (SLA-LOG-003)
