import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  Eye,
  X,
} from "lucide-react";
import { api, safeApi } from "../api";
import {
  AsyncButton,
  Card,
  Header,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";
import { predictionView } from "../predictionView";

export default function Alerts() {
  const [rawAlerts, setRawAlerts] = useState<any[]>([]);
  const [rawPredictions, setRawPredictions] = useState<any[]>([]);
  const [selected, setSelected] = useState<any | null>(null);
  const [saving, setSaving] = useState<string | null>(null);

  async function load() {
    const [alerts, predictions] = await Promise.all([
      safeApi<any[]>("/alerts", []),
      safeApi<any[]>("/predictions", []),
    ]);
    setRawAlerts(alerts);
    setRawPredictions(predictions);
  }

  useEffect(() => {
    void load();
  }, []);

  const predictionById = useMemo(() => {
    const map = new Map<string, ReturnType<typeof predictionView>>();
    rawPredictions.map(predictionView).forEach((prediction) => {
      map.set(prediction.id, prediction);
      map.set(`prediction:${prediction.id}`, prediction);
    });
    return map;
  }, [rawPredictions]);

  const alerts = useMemo(
    () =>
      rawAlerts.map((alert) => ({
        ...alert,
        acknowledged: Boolean(alert.acknowledged),
        prediction: predictionById.get(String(alert.id)),
      })),
    [rawAlerts, predictionById],
  );

  const active = alerts.filter((alert) => !alert.acknowledged);
  const critical = active.filter(
    (alert) => String(alert.severity).toLowerCase() === "high",
  ).length;
  const acknowledged = alerts.filter((alert) => alert.acknowledged).length;

  async function acknowledge(alert: any) {
    setSaving(String(alert.id));
    try {
      await api(`/alerts/${encodeURIComponent(String(alert.id))}/acknowledge`, {
        method: "PATCH",
      });
      await load();
    } finally {
      setSaving(null);
    }
  }

  return (
    <>
      <Header
        eyebrow="OPERATIONS"
        title="Risk Alerts"
        subtitle="Actionable delay-risk signals prioritized for operational review."
      />

      <div className="metrics four">
        <Metric label="Active Alerts" value={active.length} tone="danger" />
        <Metric label="Critical" value={critical} tone="danger" />
        <Metric label="Acknowledged" value={acknowledged} tone="success" />
        <Metric label="Latest Signal" value={active.length ? "Now" : "—"} icon={<Clock3 size={16} />} />
      </div>

      <Card>
        <SectionTitle
          title="Active queue"
          subtitle="Model and event-driven signals with review and acknowledgement"
        />

        <div className="alert-queue-v2">
          {alerts.map((alert) => {
            const prediction = alert.prediction;
            return (
              <div className="alert-row-v2" key={alert.id}>
                <div className="alert-row-icon">
                  {alert.acknowledged ? <CheckCircle2 size={17} /> : <AlertTriangle size={17} />}
                </div>

                <div className="alert-row-content">
                  <b>{alert.title ?? "Supply-chain risk alert"}</b>
                  <small>
                    {prediction
                      ? `${prediction.origin ?? "—"} → ${prediction.destination ?? "—"} · ${(prediction.probability * 100).toFixed(1)}%`
                      : alert.detail ?? "Operational risk requires review."}
                  </small>
                </div>

                <RiskBadge level={alert.severity ?? "high"} />

                <button className="secondary-inline" onClick={() => setSelected(alert)}>
                  <Eye size={14} /> Review
                </button>

                <AsyncButton
                  className="text-button"
                  loading={saving === String(alert.id)}
                  loadingText="Saving"
                  disabled={alert.acknowledged}
                  onClick={() => acknowledge(alert)}
                >
                  {alert.acknowledged ? "Acknowledged" : "Acknowledge"}
                </AsyncButton>
              </div>
            );
          })}

          {!alerts.length && <div className="table-empty">No active alerts.</div>}
        </div>
      </Card>

      {selected && (
        <div className="modal-backdrop" onClick={() => setSelected(null)}>
          <div className="risk-detail-modal" onClick={(event) => event.stopPropagation()}>
            <button className="modal-close" onClick={() => setSelected(null)}>
              <X size={17} />
            </button>

            <span className="side-panel-kicker">RISK REVIEW</span>
            <h2>{selected.title ?? "Supply-chain alert"}</h2>
            <p>{selected.detail ?? "Operational risk requires review."}</p>

            {selected.prediction && (
              <div className="risk-detail-score">
                <strong>{(selected.prediction.probability * 100).toFixed(1)}%</strong>
                <div>
                  <RiskBadge level={selected.prediction.riskLevel} />
                  <span
                    className={
                      selected.prediction.isDelayed
                        ? "prediction-decision delayed"
                        : "prediction-decision on-track"
                    }
                  >
                    {selected.prediction.decisionLabel}
                  </span>
                </div>
              </div>
            )}

            <div className="risk-next-steps">
              <h3>Recommended next steps</h3>
              <ol>
                <li>Validate route weather and external disruption intelligence.</li>
                <li>Review alternate service-level or carrier options.</li>
                <li>Assign the shipment for active operational monitoring.</li>
                <li>Prepare proactive customer communication if the risk persists.</li>
              </ol>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
