---
document: Warehouse Operations Procedure
document_id: SOP-WH-005
version: 2.4
owner: Warehouse Operations
effective_date: 2026-06-15
review_cycle: Semi-annual
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Warehouse Operations Procedure

## 1. Purpose

This procedure governs day-to-day operations across Meridian distribution centers: site profiles, operating hours, dock scheduling, dispatch cut-offs, and inventory thresholds. It supports the service commitments in `shipping_policy.md`.

## 2. Site profiles

| Site | Code | Dock doors | Area (sq ft) | Outbound capacity/day | Operating hours (local) |
|---|---|---|---|---|---|
| Dallas, TX | DC-DAL | 42 | 480,000 | ~18,000 | 06:00–22:00, Mon–Sat |
| Chicago, IL | DC-CHI | 36 | 410,000 | ~15,000 | 06:00–22:00, Mon–Sat |
| Los Angeles, CA | DC-LAX | 48 | 520,000 | ~21,000 | 05:00–23:00, Mon–Sun |
| New York, NY | DC-NYC | 24 | 260,000 | ~9,000 | 06:00–20:00, Mon–Fri |

## 3. Shift pattern

Each site runs an inbound-weighted morning shift and an outbound-weighted afternoon/evening shift. Outbound staging must be complete 30 minutes before each service level's cut-off (`shipping_policy.md`).

## 4. Dock scheduling

1. Inbound and outbound docks are booked in 30-minute slots. Carriers without a booking are handled first-available after booked slots.
2. Outbound dispatch is prioritized by service level: Same Day, then First Class, then Second Class, then Standard Class.
3. An order not staged by its cut-off rolls to the next business day and is flagged for review if it carries Elevated or High delay risk.

## 5. Inventory thresholds

Each SKU at each site carries a reorder point and a safety-stock floor.

| Threshold | Definition | Action |
|---|---|---|
| Reorder point | Stock covering lead time plus safety stock | Raise a replenishment order |
| Low-stock alert | On-hand below 15% of monthly demand | Notify site planner; review open shipments |
| Out-of-stock risk | On-hand below safety-stock floor | Escalate to Warehouse Lead; hold affected commitments |

## 6. Capacity management

When a site exceeds 90% of usable pick-face capacity, inbound bookings for slow-moving SKUs are deferred and cross-dock volume is prioritized to protect outbound throughput. DC-NYC, the smallest site, cross-docks priority Northeast volume during peak rather than storing it.

## 7. Special handling

Temperature-controlled and hazardous goods are staged in designated zones and must ship on a service level whose transit window stays within the product's stability window. These shipments cannot be rolled to the next day without a Warehouse Lead sign-off.

## 8. Disruption handling

When a disruption affects a site's region, the site follows `disruption_response_playbook.md`: confirm affected outbound shipments, re-sequence dispatch to protect at-risk commitments, and log the event. Reroutes that would move a shipment to a service level exceeding a product's stability window are prohibited; hold instead.

## 9. Performance measures

| KPI | Target |
|---|---|
| Same-day dispatch compliance | ≥ 99% |
| Average outbound dock turnaround | ≤ 35 minutes |
| Dispatch accuracy (correct item/quantity/address) | ≥ 99.5% |
| Inventory record accuracy | ≥ 98% |

## Related documents

- `shipping_policy.md` — cut-offs and service levels
- `disruption_response_playbook.md` — site-level disruption response

## Revision history

| Version | Date | Change |
|---|---|---|
| 2.4 | 2026-06-15 | Added site-profile capacities, shift pattern, and KPIs |
| 2.3 | 2026-01-30 | Added cross-dock rule for DC-NYC peak |
| 2.0 | 2025-08-01 | Standardized dock-scheduling across sites |
