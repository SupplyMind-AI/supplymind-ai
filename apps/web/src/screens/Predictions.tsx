import { useEffect, useMemo, useState } from "react";
import { Filter, PackagePlus } from "lucide-react";
import { safeApi } from "../api";
import { Card, Header, Metric, RiskBadge, SectionTitle } from "../components";
import { predictionView } from "../predictionView";

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

  const predictions = useMemo(() => data.map(predictionView), [data]);
  const shown =
    risk === "all"
      ? predictions
      : predictions.filter((item) => item.riskLevel === risk);

  const delayed = predictions.filter((x) => x.isDelayed).length;
  const high = predictions.filter((x) => x.riskLevel === "high").length;
  const medium = predictions.filter((x) => x.riskLevel === "medium").length;
  const low = predictions.filter((x) => x.riskLevel === "low").length;

  return (
    <>
      <Header
        eyebrow="SHIPMENT INTELLIGENCE"
        title="Shipment Intelligence"
        subtitle="Operational view of persisted model scores, shipment routes and predicted delivery outcomes."
        action={
          <button className="primary" onClick={onOpenIntake}>
            <PackagePlus size={15} />
            Score shipments
          </button>
        }
      />

      <div className="metrics five">
        <Metric label="Scored Shipments" value={predictions.length} />
        <Metric label="Predicted Delays" value={delayed} tone="danger" />
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
            <span>Prediction</span>
          </div>

          {shown.map((item) => (
            <div
              className="premium-table-row six interactive"
              key={item.id || item.shipmentId}
            >
              <b>{item.shipmentId}</b>
              <span>{item.origin ?? "—"}</span>
              <span>{item.destination ?? "—"}</span>
              <RiskBadge level={item.riskLevel} />
              <strong>{(item.probability * 100).toFixed(1)}%</strong>
              <span
                className={
                  item.isDelayed
                    ? "prediction-decision delayed"
                    : "prediction-decision on-track"
                }
              >
                {item.decisionLabel}
              </span>
            </div>
          ))}

          {!shown.length && (
            <div className="table-empty">No predictions match this filter.</div>
          )}
        </div>
      </Card>
    </>
  );
}
