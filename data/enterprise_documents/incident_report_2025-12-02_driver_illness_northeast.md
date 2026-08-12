---
document: Incident Report — Driver Illness, Northeast Route
document_id: INC-2025-083
incident_date: 2025-12-02
event_type: carrier_operational
severity: 0.25
sites_affected: [DC-NYC]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Driver Illness, Northeast Route (INC-2025-083)

## Summary

On 2 December 2025, a Keystone Express driver fell ill partway through a Northeast delivery route, delaying the shipments on that vehicle by several hours. This was a carrier operational event (severity 0.25, Minor), not an external disruption: the carrier resolved it with a driver reassignment while Meridian monitored the affected shipments. It is recorded to show that low-severity operational events are handled without escalation.

## Timeline

| Time (local) | Event |
|---|---|
| Dec 02, 09:15 | Driver reports illness mid-route; vehicle paused |
| Dec 02, 09:40 | Keystone Express dispatches a replacement driver from a nearby depot |
| Dec 02, 11:20 | Route resumes; SupplyMind updates affected shipment ETAs |
| Dec 02, 16:00 | All shipments delivered; three narrowly outside window |

## Affected scope

- 14 shipments on a single Northeast route.
- No site-wide or lane-wide impact; a single-vehicle delay.

## Root cause

An individual driver illness — a routine carrier capacity event. The carrier held responsibility for resolution; there was no routing, weather, or supplier cause.

## Mitigation

1. **Carrier resolution** — Keystone Express reassigned a replacement driver from a nearby depot; Meridian did not reroute.
2. **Monitoring** — Logistics Operations monitored the 14 affected shipments and updated ETAs; no escalation, as no committed window for a contractual account was breached.
3. **No systemic action** — the event did not meet the threshold for a disruption response.

## Impact

- 3 of 14 shipments delivered narrowly outside their window; all were non-contractual Standard Class.
- No service credit; no force-majeure relevance.
- No measurable effect on the DC-NYC on-time rate.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Note carrier driver-backup coverage in the next Keystone review | Procurement | 2026-01-31 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006), carrier operational events
- `delay_escalation_policy.md` (POL-DEL-002)
