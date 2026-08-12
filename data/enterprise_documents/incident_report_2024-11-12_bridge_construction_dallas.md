---
document: Incident Report — Bridge Construction Closure, DC-DAL
document_id: INC-2024-078
incident_date: 2024-11-12
event_type: construction
severity: 0.55
sites_affected: [DC-DAL]
owner: Logistics Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Bridge Construction Closure, DC-DAL (INC-2024-078)

## Summary

Beginning 12 November 2024, a scheduled three-week bridge rehabilitation closed a key crossing on a Central corridor lane used by DC-DAL. Because the closure dates were published in advance, it was handled as a planned infrastructure event (severity 0.55, Moderate) with a standing reroute for the duration rather than a per-shipment response. Handled under `disruption_response_playbook.md` as infrastructure / construction closure.

## Timeline

| Date | Event |
|---|---|
| Nov 03 | Closure schedule published; affected lane identified |
| Nov 10 | Standing reroute configured in SupplyMind lane settings; ETAs revised |
| Nov 12 | Closure begins; all affected volume uses the reroute automatically |
| Dec 03 | Bridge reopens; standing reroute removed; lane restored |

## Affected scope

- One Central corridor lane for a three-week window.
- All DC-DAL outbound using the affected crossing (Second Class and Standard Class primarily).
- Committed windows for the lane extended by an average of half a business day for the duration.

## Root cause

Planned public-infrastructure rehabilitation with a known schedule. Predictable and time-bounded, so the response was a configuration change, not repeated manual intervention.

## Mitigation

1. **Standing reroute** — configured an alternate crossing for the affected lane in SupplyMind for the closure window, so rerouting was automatic.
2. **Window adjustment** — revised committed transit windows for the lane and communicated updated ETAs to affected accounts in advance.
3. **Lane configuration** — updated lane settings so predictions and monitoring reflected the temporary routing.
4. **Scheduled removal** — set the reroute to be removed on reopening to avoid stale routing.

## Impact

- Affected-lane on-time held against the adjusted windows; no credits triggered.
- No force-majeure claim; the closure was planned and mitigated in advance.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Add a published-roadworks feed to lane planning | Logistics Operations | 2024-12-20 |
| Document the standing-reroute procedure for scheduled closures | Logistics Operations Lead | 2025-01-15 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `shipping_policy.md` (POL-SHP-001)
- `logistics_sla.md` (SLA-LOG-003)
