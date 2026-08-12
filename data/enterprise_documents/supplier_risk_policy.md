---
document: Supplier Risk Policy
document_id: POL-SUP-004
version: 1.2
owner: Procurement & Supplier Management
effective_date: 2026-05-15
review_cycle: Annual
classification: Internal
status: SIMULATED — created for the SupplyMind AI capstone; not a real company policy
---

# Supplier Risk Policy

## 1. Purpose

This policy defines how Meridian Logistics scores supplier risk, how often each supplier is reviewed, and what corrective action applies when a supplier underperforms. Supplier risk is a leading indicator of downstream shipment delay.

## 2. Supplier risk score

Each active supplier carries a risk score from 0 (lowest risk) to 100 (highest risk), recalculated monthly as a weighted sum of four normalized components, each scored 0–100:

`risk_score = 0.40·delivery + 0.25·quality + 0.20·variability + 0.15·exposure`

| Component | Weight | Definition |
|---|---|---|
| Delivery | 40% | Inverse of rolling 90-day on-time delivery rate against agreed lead time |
| Quality | 25% | Defect / rejection rate at inbound inspection |
| Variability | 20% | Standard deviation of actual vs agreed lead time |
| Exposure | 15% | Exposure to regions with active or recurring disruptions |

## 3. Risk tiers

| Tier | Score | Meaning | Review cadence |
|---|---|---|---|
| A | 0–24 | Low risk | Quarterly |
| B | 25–49 | Moderate risk | Monthly |
| C | 50–74 | High risk | Fortnightly, with a corrective plan |
| D | 75–100 | Critical risk | Weekly, with sourcing contingency active |

## 4. Example calculation

A supplier with delivery = 55, quality = 40, variability = 60, exposure = 70:

`0.40·55 + 0.25·40 + 0.20·60 + 0.15·70 = 22 + 10 + 12 + 10.5 = 54.5` → **Tier C (High risk)**.

The supplier enters a Performance Improvement Plan and moves to fortnightly review.

## 5. Corrective action

A supplier that enters Tier C or above is placed on a Performance Improvement Plan (PIP) owned by Supplier Management:

1. Document the specific failures and their delivery impact.
2. Agree measurable recovery targets and a review date.
3. Divert new critical volume to an approved alternate while the PIP is open.
4. Close the PIP only after two consecutive review periods back in Tier B or better.

## 6. Onboarding

New suppliers must score Tier B or better on an initial assessment before receiving production volume, and pass this checklist:

- Signed service agreement with agreed lead times.
- Quality inspection plan and defect thresholds.
- Business-continuity and disruption-exposure declaration.
- A named alternate for any single-source critical line.

A new supplier is capped at 20% of any single product line's volume for its first 90 days.

## 7. Escalation

A supplier reaching Tier D, or two Tier-C suppliers on the same critical product line, is escalated to the Head of Supply Chain for a sourcing-contingency decision. Regional disruption exposure is assessed against `disruption_response_playbook.md` and the incident record.

## 8. Performance measures

| KPI | Target |
|---|---|
| Suppliers in Tier A or B | ≥ 85% |
| Overdue Tier-C/D reviews | 0 |
| Critical lines with a qualified alternate | 100% |

## Related documents

- `disruption_response_playbook.md` — regional disruption exposure
- `logistics_sla.md` — downstream on-time impact

## Revision history

| Version | Date | Change |
|---|---|---|
| 1.2 | 2026-05-15 | Added scoring formula, example, and onboarding checklist |
| 1.1 | 2025-12-05 | Added Tier-D weekly review and sourcing contingency |
| 1.0 | 2025-06-01 | Initial issue |
