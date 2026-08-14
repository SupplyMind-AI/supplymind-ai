import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BellRing,
  CircleCheck,
  Clock3,
} from "lucide-react";
import { safeApi } from "../api";
import {
  Card,
  Header,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);

  useEffect(() => {
    void Promise.all([
      safeApi<any[]>("/alerts", []),
      safeApi<any[]>("/predictions", []),
    ]).then(([alertData, predictionData]) => {
      setAlerts(alertData);
      setPredictions(predictionData);
    });
  }, []);

  const derived = useMemo(() => {
    if (alerts.length) return alerts;

    return predictions
      .filter(
        (item) =>
          Number(item.delay_probability ?? item.probability ?? 0) >= 0.7,
      )
      .map((item, index) => ({
        id: item.id ?? index,
        title: `High delay risk · ${
          item.external_id ?? item.shipment_id ?? "Shipment"
        }`,
        description: `Champion model score ${(
          Number(item.delay_probability ?? item.probability ?? 0) * 100
        ).toFixed(1)}%.`,
        severity: "high",
      }));
  }, [alerts, predictions]);

  return (
    <>
      <Header
        eyebrow="OPERATIONS"
        title="Risk Alerts"
        subtitle="Actionable delay-risk signals prioritized for operational review."
      />

      <div className="metrics four">
        <Metric
          label="Active Alerts"
          value={derived.length}
          tone="danger"
          icon={<BellRing size={16} />}
        />
        <Metric
          label="Critical"
          value={
            derived.filter(
              (a) =>
                String(a.severity ?? a.risk_level).toLowerCase() ===
                "high",
            ).length
          }
          tone="danger"
        />
        <Metric
          label="Acknowledged"
          value="0"
          tone="success"
          icon={<CircleCheck size={16} />}
        />
        <Metric
          label="Latest Signal"
          value={derived.length ? "Now" : "—"}
          icon={<Clock3 size={16} />}
        />
      </div>

      <Card>
        <SectionTitle
          title="Active queue"
          subtitle="Model and event-driven risk signals"
        />
        <div className="alert-feed">
          {derived.map((alert, index) => (
            <div className="alert-feed-row" key={alert.id ?? index}>
              <div className="alert-feed-icon">
                <AlertTriangle size={16} />
              </div>
              <div>
                <b>{alert.title ?? "Supply-chain risk alert"}</b>
                <p>
                  {alert.description ??
                    alert.message ??
                    "Operational risk requires review."}
                </p>
              </div>
              <RiskBadge
                level={alert.severity ?? alert.risk_level ?? "high"}
              />
              <button className="text-button">View details →</button>
            </div>
          ))}
          {!derived.length && (
            <div className="table-empty">No active alerts.</div>
          )}
        </div>
      </Card>
    </>
  );
}
