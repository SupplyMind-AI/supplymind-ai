---
document: Incident Report — Public Health Outbreak, DC-CHI
document_id: INC-2020-011
incident_date: 2020-02-19
event_type: public_health
severity: 0.68
sites_affected: [DC-CHI]
owner: Warehouse Operations
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Public Health Outbreak, DC-CHI (INC-2020-011)

## Summary

From 19 February 2020, a seasonal respiratory outbreak (a circulating COVID variant) caused sustained staff absence at DC-CHI, peaking at roughly 30% of the warehouse workforce over a ten-day period. This was a labor-capacity disruption, not a transport event: shipments could be picked and dispatched, but not at full throughput. Handled under `disruption_response_playbook.md` as a public health event (severity 0.68, Moderate).

## Timeline

| Date | Event |
|---|---|
| Feb 19 | Absence crosses 20% of shift; site flags reduced outbound capacity |
| Feb 20 | Cross-site load balancing begins: overflow routed to DC-DAL |
| Feb 21 | Temporary agency staff onboarded for pick/pack |
| Feb 24 | Non-priority Standard Class cut-offs extended by one day |
| Mar 01 | Absence normalizes; DC-CHI returns to full throughput |

## Affected scope

- DC-CHI outbound throughput reduced by an estimated 25–30% for ten days.
- Midwest and Northeast Standard Class most affected; Same Day and First Class protected.
- No single shipment lost; the risk was aggregate throughput, not routing.

## Root cause

Workforce absence from a respiratory outbreak. No transport, carrier, or supplier fault. The constraint was pick/pack labor, so mitigation targeted capacity and prioritization rather than routing.

## Mitigation

1. **Cross-site load balancing** — shifted overflow Midwest/Northeast volume to DC-DAL, which had spare capacity.
2. **Temporary staffing** — onboarded agency pickers to cover the shift gap.
3. **Prioritization** — protected Same Day, First Class, and all contractual accounts; extended cut-offs only for non-priority Standard Class.
4. **Health measures** — staggered shifts and sick-leave enforcement to limit spread.

## Impact

- DC-CHI weekly on-time rate dipped to 94.0%, above Silver but below Gold target.
- No Gold or Platinum account fell below its contractual target, so no credits were triggered.
- No force-majeure claim; a staffing shortage with available mitigation is not an excludable event.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Write a pandemic/absence continuity plan (cross-site load thresholds) | Warehouse Operations | 2020-04-15 |
| Cross-train staff across pick zones to reduce single-role dependency | Site Leads | 2020-05-01 |
| Pre-agree an agency-staffing surge contract | Procurement | 2020-04-30 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `warehouse_operations.md` (SOP-WH-005)
- `logistics_sla.md` (SLA-LOG-003)
