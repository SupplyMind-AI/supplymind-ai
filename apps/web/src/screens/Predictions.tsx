import { useEffect, useMemo, useState } from "react";
import {
  Filter,
  PackagePlus,
} from "lucide-react";

import { safeApi } from "../api";
import {
  Card,
  Header,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";
import { predictionView } from "../predictionView";

export default function Predictions({
  onOpenIntake,
}: {
  onOpenIntake: () => void;
}) {
  const [data, setData] = useState<any[]>([]);
  const [risk, setRisk] = useState("all");
  const [decision, setDecision] = useState("all");

  useEffect(() => {
    void safeApi<any[]>("/predictions", []).then(setData);
  }, []);

  const normalized = useMemo(
    () => data.map(predictionView),
    [data],
  );

  const shown = useMemo(
    () =>
      normalized.filter((item) => {
        const riskMatch =
          risk === "all" || item.riskLevel === risk;

        const decisionMatch =
          decision === "all" ||
          (decision === "delay" && item.isDelayed) ||
          (decision === "track" && !item.isDelayed);

        return riskMatch && decisionMatch;
      }),
    [normalized, risk, decision],
  );

  const delayed = normalized.filter((x) => x.isDelayed).length;
  const high = normalized.filter((x) => x.riskLevel === "high").length;
  const medium = normalized.filter((x) => x.riskLevel === "medium").length;
  const low = normalized.filter((x) => x.riskLevel === "low").length;

  return (
    <>
      <Header
        eyebrow="SHIPMENT INTELLIGENCE"
        title="Shipment Intelligence"
        subtitle="Operational view of persisted model scores, routes and predicted delivery outcomes."
        action={
          <button className="primary" onClick={onOpenIntake}>
            <PackagePlus size={15} />
            Score shipments
          </button>
        }
      />

      <div className="metrics five compact-metrics">
        <Metric label="Scored" value={normalized.length} />
        <Metric label="Delay likely" value={delayed} tone="danger" />
        <Metric label="High risk" value={high} tone="danger" />
        <Metric label="Medium risk" value={medium} tone="warning" />
        <Metric label="Low risk" value={low} tone="success" />
      </div>

      <Card className="compact-card">
        <SectionTitle
          title="Shipment Risk List"
          subtitle={`${shown.length} of ${normalized.length} predictions shown`}
          action={
            <div className="filter-row compact-filter-row">
              <Filter size={14} />

              <select value={risk} onChange={(e) => setRisk(e.target.value)}>
                <option value="all">All risk levels</option>
                <option value="high">High risk</option>
                <option value="medium">Medium risk</option>
                <option value="low">Low risk</option>
              </select>

              <select
                value={decision}
                onChange={(e) => setDecision(e.target.value)}
              >
                <option value="all">All predictions</option>
                <option value="delay">Delay likely</option>
                <option value="track">On track</option>
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

          {shown.map((item, index) => (
            <div
              className="premium-table-row six interactive"
              key={item.id || `${item.shipmentId}-${index}`}
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
            <div className="table-empty">
              No predictions match these filters.
            </div>
          )}
        </div>
      </Card>
    </>
  );
}
