import { useEffect, useMemo, useState } from "react";
import {
  ArrowUpRight,
  Filter,
  PackagePlus,
  Sparkles,
} from "lucide-react";
import { safeApi } from "../api";
import {
  Card,
  Header,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";

export default function Predictions({
  onOpenIntake,
}: {
  onOpenIntake: () => void;
}) {
  const [data, setData] = useState<any[]>([]);
  const [risk, setRisk] = useState("all");

  useEffect(() => {
    void safeApi<any[]>("/predictions", []).then(setData);
  }, []);

  const normalized = useMemo(
    () =>
      data.map((item) => {
        const probability = Number(
          item.delay_probability ??
            item.probability ??
            item.risk_score ??
            0,
        );
        const level =
          String(item.risk_level ?? "").toLowerCase() ||
          (probability >= 0.7
            ? "high"
            : probability >= 0.4
              ? "medium"
              : "low");

        return {
          ...item,
          probability,
          level,
        };
      }),
    [data],
  );

  const shown =
    risk === "all"
      ? normalized
      : normalized.filter((item) => item.level === risk);

  const high = normalized.filter((x) => x.level === "high").length;
  const medium = normalized.filter((x) => x.level === "medium").length;
  const low = normalized.filter((x) => x.level === "low").length;

  return (
    <>
      <Header
        eyebrow="SHIPMENT INTELLIGENCE"
        title="Predictions"
        subtitle="Operational view of persisted model scores, risk levels and shipment priorities."
        action={
          <button className="primary" onClick={onOpenIntake}>
            <PackagePlus size={15} />
            Score shipments
          </button>
        }
      />

      <div className="metrics four">
        <Metric label="Scored Shipments" value={normalized.length} />
        <Metric label="High Risk" value={high} tone="danger" />
        <Metric label="Medium Risk" value={medium} tone="warning" />
        <Metric label="Low Risk" value={low} tone="success" />
      </div>

      <Card>
        <SectionTitle
          title="Shipment Risk List"
          subtitle="Filter and investigate model decisions"
          action={
            <div className="filter-row">
              <Filter size={14} />
              <select value={risk} onChange={(e) => setRisk(e.target.value)}>
                <option value="all">All risk levels</option>
                <option value="high">High risk</option>
                <option value="medium">Medium risk</option>
                <option value="low">Low risk</option>
              </select>
            </div>
          }
        />

        <div className="premium-table">
          <div className="premium-table-head six">
            <span>Shipment</span>
            <span>Origin</span>
            <span>Destination</span>
            <span>Risk</span>
            <span>Probability</span>
            <span>Decision</span>
          </div>

          {shown.map((item, index) => (
            <div
              className="premium-table-row six interactive"
              key={item.id ?? index}
            >
              <b>
                {item.external_id ??
                  item.shipment_id ??
                  item.id ??
                  `Shipment ${index + 1}`}
              </b>
              <span>{item.origin_city ?? item.customer_city ?? "—"}</span>
              <span>{item.destination_city ?? item.order_city ?? "—"}</span>
              <RiskBadge level={item.level} />
              <strong>{(item.probability * 100).toFixed(1)}%</strong>
              <span className="decision-link">
                {item.is_delayed ?? item.predicted_delay
                  ? "Delay"
                  : "On track"}
                <ArrowUpRight size={13} />
              </span>
            </div>
          ))}

          {!shown.length && (
            <div className="table-empty">
              No predictions match this filter.
            </div>
          )}
        </div>
      </Card>
    </>
  );
}
