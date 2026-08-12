---
document: Incident Report — Hurricane, Northeast Corridor, DC-NYC
document_id: INC-2021-057
incident_date: 2021-09-03
event_type: severe_weather
severity: 0.90
sites_affected: [DC-NYC]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Hurricane, Northeast Corridor, DC-NYC (INC-2021-057)

## Summary

On 3 September 2021, a hurricane tracked toward the Northeast corridor and made landfall near the New York metro. Unlike the January winter storm (INC-2019-004), a 48-hour forecast lead allowed proactive pre-positioning before conditions deteriorated. Carriers suspended operations and area airports closed at peak. SupplyMind flagged the event at severity 0.90 (Major). Handled under `disruption_response_playbook.md`.

## Timeline

| Date | Event |
|---|---|
| Sep 01 | 48-hour forecast; pre-positioning plan activated for DC-NYC |
| Sep 02 | Priority and contractual volume dispatched ahead of landfall |
| Sep 03 | Landfall; Keystone Express suspends operations; airports close |
| Sep 04 | Peak conditions; remaining volume held; force-majeure assessment begins |
| Sep 06 | Carriers resume; backlog cleared; on-time recovers |

## Affected scope

- DC-NYC outbound to the Northeast during and after landfall.
- ~890 shipments in the affected window; a large share cleared pre-landfall.
- 2 Platinum and 3 Gold accounts with contractual commitments.

## Root cause

Hurricane landfall with carrier suspension and airport closure; no Meridian fault. The key difference from INC-2019-004 was forecast lead time, which enabled pre-positioning rather than reactive rerouting.

## Mitigation

1. **Forecast-lead pre-positioning** — dispatched priority and contractual volume in the 48 hours before landfall.
2. **Hold** — held remaining volume during peak conditions rather than risk vehicles and shipments.
3. **Force majeure** — declared for shipments stranded by the suspension and airport closures.
4. **Backlog sequencing** — on resumption, cleared held volume by service level and risk tier.

## Impact

- DC-NYC weekly on-time fell to 90.6% for affected accounts (before exclusions).
- 340 shipments logged as force majeure and excluded per `logistics_sla.md`; after exclusion, no account fell below target, so no credits were triggered.
- Pre-positioning protected all but a small share of contractual volume.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Formalize a hurricane-season pre-positioning SOP (forecast triggers) | Logistics Operations Lead | 2021-10-15 |
| Pre-agree Northeast surge capacity for Aug–Oct | Procurement | 2021-07-31 |
| Add forecast-lead triggers to SupplyMind weather alerts | Logistics Operations | 2021-11-01 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `delay_escalation_policy.md` (POL-DEL-002)
- `logistics_sla.md` (SLA-LOG-003)
- `incident_report_2019-01-08_winter_storm_chicago.md` (INC-2019-004)
