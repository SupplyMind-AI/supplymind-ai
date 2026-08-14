# SupplyMind AI

SupplyMind is my final project for the Ironhack AI Engineering bootcamp.

The project started from a problem I had already seen in practice while working at companies such as HelloFresh and Zalando: logistics teams deal with large amounts of operational data, but identifying a risky shipment early enough to act on it is still difficult.

A late shipment can have very different consequences depending on the business. For a meal-kit company, it can affect food quality and customer satisfaction. In e-commerce, it can mean missing a one-day or two-day delivery promise.

I wanted to explore how machine learning and generative AI could be combined to identify these risks earlier and give operations teams useful context around them.

SupplyMind is therefore not just a delay prediction model. It is an operational intelligence application that combines shipment predictions, external signals and internal company knowledge.

## What it does

The current version supports the following workflows:

- Create or import parcel shipments and score them with the trained delay model
- View persisted predictions and risk levels in Shipment Intelligence
- Prioritize high-risk shipments through Risk Alerts
- Review and acknowledge operational alerts
- Explore external disruption signals through the Event Monitor
- Search internal policies and operational documents using semantic search
- Generate grounded answers from retrieved enterprise knowledge using RAG
- Ask shipment and operations questions through the AI Assistant
- View operational orders, inventory and supplier reference data
- Monitor live prediction distribution and available model-monitoring information
- Expose a retraining workflow for the ML lifecycle

Some supplier and enterprise documents in the demo are simulated reference data. They are kept separate from live and persisted application data.

## Architecture

The application is split into a React frontend and a FastAPI backend.

```text
React / TypeScript
        |
        v
     FastAPI
        |
        +--------------------+
        |                    |
        v                    v
 Operational data       AI orchestration
 / predictions          and RAG
        |                    |
        v                    +---- Pinecone
   ML champion               |
                             +---- External intelligence
