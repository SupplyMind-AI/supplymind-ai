# Enterprise documents (RAG corpus)

This folder holds the unstructured enterprise knowledge that SupplyMind's semantic search and AI assistant retrieve. It is the counterpart to the structured operational data (SynDelay, PostgreSQL, model predictions, weather, GDELT events): the structured side tells the assistant *what* the risk is; these documents tell it *what to do about it* and *what happened before*.

**These are simulated documents.** They were written for the SupplyMind AI capstone and represent the internal knowledge base of a fictional operating company, **Meridian Logistics**. They are not real company policies and contain no real customer, supplier, or financial data. Each file states this in its front matter.

## Contents

**Policies, SLA, and procedures**

| File | Type | What it answers |
|---|---|---|
| `shipping_policy.md` | Policy | Service levels, transit times, order cut-offs, carrier allocation |
| `delay_escalation_policy.md` | Policy | Who reviews a shipment at each risk level, and when to escalate |
| `logistics_sla.md` | SLA | On-time targets, response commitments, delay credits, account tiers |
| `supplier_risk_policy.md` | Policy | How suppliers are scored, reviewed, and remediated |
| `warehouse_operations.md` | SOP | Site profiles, dock scheduling, inventory thresholds, KPIs |
| `disruption_response_playbook.md` | Playbook | Response to weather, strikes, congestion, and other events |

**Incident reports (dated precedents, 2019–2026)**

| File | Date | Event | Severity |
|---|---|---|---|
| `incident_report_2019-01-08_winter_storm_chicago.md` | 2019-01-08 | Severe weather (winter storm), DC-CHI | 0.84 |
| `incident_report_2020-02-19_public_health_outbreak_chicago.md` | 2020-02-19 | Public health outbreak (staffing), DC-CHI | 0.68 |
| `incident_report_2021-03-22_port_congestion_los_angeles.md` | 2021-03-22 | Port congestion, LA/Long Beach | 0.72 |
| `incident_report_2021-09-03_hurricane_northeast.md` | 2021-09-03 | Severe weather (hurricane), DC-NYC | 0.90 |
| `incident_report_2022-04-05_armed_conflict_air_corridor.md` | 2022-04-05 | Armed conflict / airspace closure (imports), DC-LAX | 0.83 |
| `incident_report_2022-05-30_carrier_strike_northeast.md` | 2022-05-30 | Strike (carrier labor action), DC-NYC | 0.88 |
| `incident_report_2023-06-20_sports_parade_chicago.md` | 2023-06-20 | Planned event (championship parade), DC-CHI | 0.42 |
| `incident_report_2023-08-01_music_festival_new_york.md` | 2023-08-01 | Planned event (music festival), DC-NYC | 0.48 |
| `incident_report_2023-10-08_wildfire_los_angeles.md` | 2023-10-08 | Wildfire / highway closure, DC-LAX | 0.66 |
| `incident_report_2024-06-11_civil_unrest_los_angeles.md` | 2024-06-11 | Civil unrest / curfew, DC-LAX | 0.71 |
| `incident_report_2024-11-12_bridge_construction_dallas.md` | 2024-11-12 | Infrastructure / construction closure, DC-DAL | 0.55 |
| `incident_report_2025-12-02_driver_illness_northeast.md` | 2025-12-02 | Carrier operational (driver illness), Northeast route | 0.25 |
| `incident_report_2026-07-14_flooding_gulf_coast.md` | 2026-07-14 | Flooding, Gulf Coast / Houston corridor | 0.79 |

## Company canon (shared by every document)

**Distribution centers**

| Site | Code | Dock doors | Region |
|---|---|---|---|
| Dallas, TX | DC-DAL | 42 | Central US |
| Chicago, IL | DC-CHI | 36 | Midwest / Northeast |
| Los Angeles, CA | DC-LAX | 48 | West Coast |
| New York, NY | DC-NYC | 24 | Northeast |

**Carriers**

| Carrier | Coverage | Role |
|---|---|---|
| Vanguard Freight | National | Primary national, Northeast surge |
| Cascade Carriers | West | Primary West Coast |
| Keystone Express | Northeast | Primary Northeast |
| Lone Star Logistics | Central | Primary Central |
| GreatLakes Transit | Midwest | Primary Midwest |

**Delay-risk tiers** (from the model's predicted delay probability `p`)

| Tier | `p` | Owner | Response SLA |
|---|---|---|---|
| Low | `< 0.40` | Automated monitoring | Daily review |
| Elevated | `0.40 – 0.69` | Logistics Operations Analyst | 8 business hours |
| High | `≥ 0.70` | Logistics Operations Lead | 4 business hours |
| High + active disruption | — | Regional Logistics Manager | 2 business hours |
| Contractual breach imminent | — | Head of Supply Chain | 1 hour |

**Event severity bands** (external disruptions, severity `0.0–1.0`): Minor `< 0.40`, Moderate `0.40–0.69`, Major `≥ 0.70`.

**Business hours** (SLA clock): 06:00–20:00 local, Monday–Saturday.

## How these are used

```
data/enterprise_documents/  ->  document loader  ->  chunking  ->  embeddings
     ->  Pinecone  ->  semantic search / RAG  ->  AI assistant
```

Files are plain Markdown so they chunk cleanly by section. YAML front matter (`document_id`, `version`, `owner`, `effective_date`) is preserved as chunk metadata so the assistant can cite a specific document and version.
