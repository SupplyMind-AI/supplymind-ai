import { useEffect, useState } from "react";
import { Boxes, Building2, PackageCheck } from "lucide-react";
import { safeApi } from "../api";
import { Card, Header, RiskBadge, SectionTitle } from "../components";

type Tab = "orders" | "inventory" | "suppliers";

export default function Operations() {
 const [tab,setTab]=useState<Tab>("orders"); const [payload,setPayload]=useState<any>({items:[]}); const [loading,setLoading]=useState(true);
 useEffect(()=>{setLoading(true); void safeApi<any>(`/operations/${tab}`,{items:[]}).then(x=>{setPayload(x);setLoading(false)})},[tab]);
 const items=payload.items ?? [];
 return <>
  <Header eyebrow="ERP / WMS INTEGRATION LAYER" title="Operations Hub" subtitle="Orders use live shipment data. Inventory flow is derived from orders; supplier rows are clearly labelled demo reference data until ERP integration." />
  <div className="segmented operations-tabs">
   <button className={tab==="orders"?"active":""} onClick={()=>setTab("orders")}><PackageCheck size={16}/>Orders</button>
   <button className={tab==="inventory"?"active":""} onClick={()=>setTab("inventory")}><Boxes size={16}/>Inventory</button>
   <button className={tab==="suppliers"?"active":""} onClick={()=>setTab("suppliers")}><Building2 size={16}/>Suppliers</button>
  </div>
  <Card>
   <SectionTitle title={tab[0].toUpperCase()+tab.slice(1)} subtitle={payload.note ?? `Data mode: ${payload.data_mode ?? "loading"}`} />
   {loading ? <div className="operations-loader"><span/><b>Loading operational data</b></div> : tab==="orders" ? <div className="premium-table"><div className="premium-table-head six"><span>Order</span><span>Route</span><span>Product</span><span>Mode</span><span>Qty</span><span>Sales</span></div>{items.map((x:any)=><div className="premium-table-row six" key={x.id}><b>{x.external_id}</b><span>{x.customer_city ?? "—"} → {x.order_city ?? "—"}</span><span>{x.product_name ?? "—"}</span><span>{x.shipping_mode ?? "—"}</span><span>{x.quantity ?? "—"}</span><strong>{x.sales != null ? `€${Number(x.sales).toFixed(0)}`:"—"}</strong></div>)}</div>
   : tab==="inventory" ? <div className="premium-table"><div className="premium-table-head five"><span>Product</span><span>Category</span><span>Observed units</span><span>Orders</span><span>Stock</span></div>{items.map((x:any,index:number)=><div className="premium-table-row five" key={index}><b>{x.product_name}</b><span>{x.category ?? "—"}</span><strong>{Number(x.observed_units).toFixed(0)}</strong><span>{x.orders}</span><span className="integration-needed">Connector required</span></div>)}</div>
   : <div className="supplier-grid">{items.map((x:any)=><article className="supplier-card" key={x.id}><div><span>{x.id}</span><h3>{x.name}</h3><p>{x.region} · {x.category}</p></div><RiskBadge level={x.risk}/><dl><div><dt>Lead time</dt><dd>{x.lead_time_days}d</dd></div><div><dt>Reliability</dt><dd>{Math.round(x.reliability*100)}%</dd></div></dl></article>)}</div>}
  </Card>
 </>;
}
