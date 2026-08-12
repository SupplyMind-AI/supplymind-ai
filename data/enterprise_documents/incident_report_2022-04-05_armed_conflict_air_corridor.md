---
document: Incident Report — Armed Conflict / Air Corridor Closure
document_id: INC-2022-014
incident_date: 2022-04-05
event_type: geopolitical
severity: 0.83
sites_affected: [DC-LAX]
owner: Procurement & Supplier Management
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real incident
---

# Incident Report — Armed Conflict / Air Corridor Closure (INC-2022-014)

## Summary

On 5 April 2022, an armed conflict in an overseas region closed an air-freight corridor used to import electronic components for a West Coast supplier line. SupplyMind flagged the geopolitical event at severity 0.83 (Major) and matched it to inbound flows destined for DC-LAX. This was an inbound / sourcing disruption; the mitigation was a mode and sourcing shift rather than a domestic reroute. Handled under `disruption_response_playbook.md` as geopolitical / armed conflict.

## Timeline

| Date | Event |
|---|---|
| Apr 05 | Event ingested; affected import line flagged; air corridor closed |
| Apr 06 | Supplier moves from Tier C to Tier D on exposure and delivery slippage |
| Apr 07 | Mode shift approved: air → sea via an alternate, longer routing |
| Apr 09 | Alternate-region supplier activated for the critical component |
| Apr 21 | Buffer stock and alternate flow stabilize the line; downstream risk clears |

## Affected scope

- Inbound electronic components for one West Coast product line.
- Downstream: ~430 West Coast outbound shipments moved to Elevated risk on component availability.
- One supplier temporarily elevated to Tier D under `supplier_risk_policy.md`.

## Root cause

External armed conflict closed the air corridor; no Meridian fault. Exposure was amplified by heavy reliance on a single overseas source and a single air routing for a critical component.

## Mitigation

1. **Mode shift** — moved the affected imports from air to sea via an alternate routing that avoided the conflict zone, accepting longer lead time.
2. **Alternate sourcing** — activated a qualified alternate supplier in a different region for the critical component.
3. **Buffer draw-down** — used DC-LAX buffer stock to cover the extended lead time.
4. **Insurance and route review** — flagged the line for a route-risk and insurance reassessment.

## Impact

- West Coast outbound on-time held at 95.4% via buffer and proactive management.
- No force-majeure declaration for outbound (windows were protected); inbound delay absorbed.
- Supplier spent 16 days in Tier D before reverting on two on-time alternate deliveries.

## Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Establish permanent dual-region sourcing for the critical line | Procurement | 2022-06-15 |
| Add geopolitical route-risk scoring to supplier exposure | Supplier Management | 2022-07-01 |
| Raise DC-LAX buffer target for conflict-exposed components | Warehouse Operations | 2022-05-10 |

## References

- `disruption_response_playbook.md` (PLB-DIS-006)
- `supplier_risk_policy.md` (POL-SUP-004)
- `warehouse_operations.md` (SOP-WH-005)
