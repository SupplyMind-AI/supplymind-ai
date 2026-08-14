from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from apps.api.dependencies import get_shipment_repository

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/orders")
async def orders(
    limit: int = Query(100, ge=1, le=200),
    repo=Depends(get_shipment_repository),
):
    rows = await repo.list_recent(limit=limit, offset=0)
    return {
        "data_mode": "live_from_shipments",
        "items": [
            {
                "id": str(row.id),
                "external_id": row.external_id,
                "order_date": row.order_date.isoformat(),
                "status": row.status or "scored",
                "customer_city": row.payload.get("customer_city"),
                "order_city": row.payload.get("order_city"),
                "order_country": row.payload.get("order_country"),
                "shipping_mode": row.payload.get("shipping_mode"),
                "product_name": row.payload.get("product_name"),
                "category_name": row.payload.get("category_name"),
                "quantity": row.payload.get("order_item_quantity"),
                "sales": row.payload.get("sales"),
            }
            for row in rows
        ],
    }


@router.get("/inventory")
async def inventory(
    limit: int = Query(200, ge=1, le=500),
    repo=Depends(get_shipment_repository),
):
    rows = await repo.list_recent(limit=limit, offset=0)
    grouped: dict[str, dict] = defaultdict(lambda: {
        "observed_units": 0.0,
        "observed_sales": 0.0,
        "orders": 0,
        "category": None,
    })

    for row in rows:
        product = str(row.payload.get("product_name") or "Unspecified product")
        item = grouped[product]
        item["observed_units"] += float(row.payload.get("order_item_quantity") or 0)
        item["observed_sales"] += float(row.payload.get("sales") or 0)
        item["orders"] += 1
        item["category"] = item["category"] or row.payload.get("category_name")

    return {
        "data_mode": "derived_from_orders",
        "note": "Current dataset has no warehouse stock-on-hand field; this view reports observed product flow rather than fabricated stock.",
        "items": [
            {
                "product_name": product,
                **values,
                "stock_on_hand": None,
                "stock_status": "inventory_connector_required",
            }
            for product, values in sorted(
                grouped.items(),
                key=lambda pair: pair[1]["observed_units"],
                reverse=True,
            )
        ],
    }


@router.get("/suppliers")
async def suppliers():
    return {
        "data_mode": "demo_reference",
        "note": "Supplier master data is not present in SynDelay. These rows are clearly labelled presentation seed data for the future ERP/supplier integration.",
        "items": [
            {"id": "SUP-001", "name": "Nordic Components AB", "region": "Northern Europe", "category": "Electronics", "lead_time_days": 4, "reliability": 0.96, "risk": "low"},
            {"id": "SUP-002", "name": "Rhine Industrial GmbH", "region": "Western Europe", "category": "Industrial Supplies", "lead_time_days": 6, "reliability": 0.91, "risk": "medium"},
            {"id": "SUP-003", "name": "Iberia Goods SL", "region": "Southern Europe", "category": "Consumer Goods", "lead_time_days": 5, "reliability": 0.94, "risk": "low"},
            {"id": "SUP-004", "name": "Baltic Freight Partners", "region": "Eastern Europe", "category": "Logistics", "lead_time_days": 8, "reliability": 0.86, "risk": "high"},
            {"id": "SUP-005", "name": "Alpine Medical AG", "region": "Western Europe", "category": "Medical Supplies", "lead_time_days": 3, "reliability": 0.98, "risk": "low"},
        ],
    }
