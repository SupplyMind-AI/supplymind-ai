import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  BellRing,
  CheckCircle2,
  Clock3,
  Eye,
  Filter,
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

type AlertView = {
  id: string;
  title: string;
  description: string;
  severity: "high" | "medium" | "low";
  probability: number | null;
  shipmentId: string | null;
  origin: string | null;
  destination: string | null;
  isDelayed: boolean | null;
  acknowledged: boolean;
  source: string;
  raw: any;
};

function normalizeAlert(alert: any, acknowledgedIds: Set<string>): AlertView {
  const id = String(alert.id ?? alert.alert_id ?? crypto.randomUUID());
  const rawProbability =
    alert.delay_probability ??
    alert.probability ??
    alert.score ??
    null;

  const probability =
    rawProbability == null || !Number.isFinite(Number(rawProbability))
      ? null
      : Number(rawProbability) > 1
        ? Number(rawProbability) / 100
        : Number(rawProbability);

  const suppliedSeverity = String(
    alert.severity ?? alert.risk_level ?? "",
  ).toLowerCase();

  const severity: "high" | "medium" | "low" =
    suppliedSeverity === "high" ||
    suppliedSeverity === "medium" ||
    suppliedSeverity === "low"
      ? suppliedSeverity
      : probability != null && probability >= 0.7
        ? "high"
        : probability != null && probability >= 0.4
          ? "medium"
          : "low";

  const backendAcknowledged =
    Boolean(alert.acknowledged) ||
    Boolean(alert.acknowledged_at) ||
    String(alert.status ?? "").toLowerCase() === "acknowledged";

  return {
    id,
    title: String(alert.title ?? "Supply-chain risk alert"),
    description: String(
      alert.description ??
        alert.message ??
        "Operational risk requires review.",
    ),
    severity,
    probability,
    shipmentId:
      alert.external_id ??
      alert.shipment_id ??
      alert.shipment?.external_id ??
      null,
    origin:
      alert.origin_city ??
      alert.customer_city ??
      alert.shipment?.customer_city ??
      alert.shipment?.features?.customer_city ??
      null,
    destination:
      alert.destination_city ??
      alert.order_city ??
      alert.shipment?.order_city ??
      alert.shipment?.features?.order_city ??
      null,
    isDelayed:
      typeof alert.delayed === "boolean"
        ? alert.delayed
        : typeof alert.is_delayed === "boolean"
          ? alert.is_delayed
          : null,
    acknowledged: backendAcknowledged || acknowledgedIds.has(id),
    source: String(alert.source ?? alert.alert_type ?? "model"),
    raw: alert,
  };
}

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [selected, setSelected] = useState<AlertView | null>(null);
  const [riskFilter, setRiskFilter] = useState("all");
  const [probabilityFilter, setProbabilityFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("open");
  const [savingId, setSavingId] = useState<string | null>(null);

  const [acknowledgedIds, setAcknowledgedIds] = useState<Set<string>>(
    () =>
      new Set(
        JSON.parse(
          localStorage.getItem("supplymind_ack_alerts") ?? "[]",
        ),
      ),
  );

  useEffect(() => {
    void Promise.all([
      safeApi<any[]>("/alerts", []),
      safeApi<any[]>("/predictions", []),
    ]).then(([alertData, predictionData]) => {
      setAlerts(alertData);
      setPredictions(predictionData);
    });
  }, []);

  const derived = useMemo<AlertView[]>(() => {
    if (alerts.length) {
      return alerts.map((alert) =>
        normalizeAlert(alert, acknowledgedIds),
      );
    }

    return predictions
      .map(predictionView)
      .filter(
        (item) =>
          item.riskLevel === "high" ||
          item.riskLevel === "medium" ||
          item.isDelayed,
      )
      .map((item) => {
        const id = item.id || item.shipmentId;

        return {
          id,
          title: `${
            item.riskLevel === "high" ? "High" : "Elevated"
          } delay risk · ${item.shipmentId}`,
          description: `Champion score ${(
            item.probability * 100
          ).toFixed(1)}% · ${item.decisionLabel}.`,
          severity: item.riskLevel,
          probability: item.probability,
          shipmentId: item.shipmentId,
          origin: item.origin,
          destination: item.destination,
          isDelayed: item.isDelayed,
          acknowledged: acknowledgedIds.has(id),
          source: "model",
          raw: item.raw,
        };
      });
  }, [alerts, predictions, acknowledgedIds]);

  const shown = useMemo(
    () =>
      derived.filter((alert) => {
        const riskMatch =
          riskFilter === "all" || alert.severity === riskFilter;

        const probabilityMatch =
          probabilityFilter === "all" ||
          (probabilityFilter === "70" &&
            alert.probability != null &&
            alert.probability >= 0.7) ||
          (probabilityFilter === "80" &&
            alert.probability != null &&
            alert.probability >= 0.8) ||
          (probabilityFilter === "90" &&
            alert.probability != null &&
            alert.probability >= 0.9);

        const statusMatch =
          statusFilter === "all" ||
          (statusFilter === "open" && !alert.acknowledged) ||
          (statusFilter === "acknowledged" && alert.acknowledged);

        return riskMatch && probabilityMatch && statusMatch;
      }),
    [derived, riskFilter, probabilityFilter, statusFilter],
  );

  const acknowledgedCount = derived.filter(
    (alert) => alert.acknowledged,
  ).length;

  const criticalCount = derived.filter(
    (alert) => alert.severity === "high",
  ).length;

  async function acknowledge(alert: AlertView) {
    setSavingId(alert.id);

    try {
      await api(`/alerts/${encodeURIComponent(alert.id)}/acknowledge`, {
        method: "PATCH",
      });
    } catch {
      // Keep the presentation interaction usable even when a deployment
      // is running the older alert router.
    }

    const next = new Set(acknowledgedIds);
    next.add(alert.id);
    setAcknowledgedIds(next);

    localStorage.setItem(
      "supplymind_ack_alerts",
      JSON.stringify([...next]),
    );

    setSelected((current) =>
      current?.id === alert.id
        ? { ...current, acknowledged: true }
        : current,
    );

    setSavingId(null);
  }

  return (
    <>
      <Header
        eyebrow="OPERATIONS"
        title="Risk Alerts"
        subtitle="Actionable delay-risk signals prioritized for operational review."
      />

      <div className="metrics four compact-metrics">
        <Metric
          label="Active alerts"
          value={derived.filter((a) => !a.acknowledged).length}
          tone="danger"
          icon={<BellRing size={16} />}
        />
        <Metric
          label="Critical"
          value={criticalCount}
          tone="danger"
          icon={<AlertTriangle size={16} />}
        />
        <Metric
          label="Acknowledged"
          value={acknowledgedCount}
          tone="success"
          icon={<CheckCircle2 size={16} />}
        />
        <Metric
          label="Latest signal"
          value={derived.length ? "Now" : "—"}
          icon={<Clock3 size={16} />}
        />
      </div>

      <Card className="compact-card">
        <SectionTitle
          title="Active queue"
          subtitle={`${shown.length} risk signals match the current filters`}
          action={
            <div className="filter-row compact-filter-row">
              <Filter size={14} />

              <select
                value={riskFilter}
                onChange={(e) => setRiskFilter(e.target.value)}
              >
                <option value="all">All risk</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>

              <select
                value={probabilityFilter}
                onChange={(e) => setProbabilityFilter(e.target.value)}
              >
                <option value="all">Any probability</option>
                <option value="70">70%+</option>
                <option value="80">80%+</option>
                <option value="90">90%+</option>
              </select>

              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              >
                <option value="open">Open</option>
                <option value="acknowledged">Acknowledged</option>
                <option value="all">All status</option>
              </select>
            </div>
          }
        />

        <div className="alert-feed premium-alert-feed">
          {shown.map((alert) => (
            <div
              className={`alert-feed-row premium-alert-row ${
                alert.acknowledged ? "acknowledged" : ""
              }`}
              key={alert.id}
            >
              <div className="alert-feed-icon">
                {alert.acknowledged ? (
                  <CheckCircle2 size={16} />
                ) : (
                  <AlertTriangle size={16} />
                )}
              </div>

              <div className="alert-copy">
                <b>{alert.title}</b>
                <p>{alert.description}</p>

                {(alert.shipmentId ||
                  alert.origin ||
                  alert.destination) && (
                  <small>
                    {alert.shipmentId ?? "Shipment"}
                    {alert.origin || alert.destination
                      ? ` · ${alert.origin ?? "—"} → ${
                          alert.destination ?? "—"
                        }`
                      : ""}
                  </small>
                )}
              </div>

              <div className="alert-score">
                <RiskBadge level={alert.severity} />
                {alert.probability != null && (
                  <strong>
                    {(alert.probability * 100).toFixed(1)}%
                  </strong>
                )}
              </div>

              <div className="alert-row-actions">
                <button
                  className="secondary-inline"
                  onClick={() => setSelected(alert)}
                >
                  <Eye size={14} />
                  Review
                </button>
                <AsyncButton
                  loading={savingId === alert.id}
                  loadingText="Saving"
                  className="alert-ack-button"
                  disabled={alert.acknowledged}
                  onClick={() => acknowledge(alert)}
                >
                  {alert.acknowledged ? "Acknowledged" : "Acknowledge"}
                </AsyncButton>
              </div>
            </div>
          ))}

          {!shown.length && (
            <div className="table-empty">
              No alerts match these filters.
            </div>
          )}
        </div>
      </Card>

      {selected && (
        <div
          className="modal-backdrop"
          onClick={() => setSelected(null)}
        >
          <div
            className="risk-detail-modal premium-risk-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <button
              className="modal-close"
              onClick={() => setSelected(null)}
            >
              <X size={17} />
            </button>

            <span className="side-panel-kicker">RISK REVIEW</span>
            <h2>{selected.shipmentId ?? selected.title}</h2>

            {(selected.origin || selected.destination) && (
              <p className="risk-modal-route">
                {selected.origin ?? "—"} → {selected.destination ?? "—"}
              </p>
            )}

            <div className="risk-detail-score">
              <div>
                <span>Delay probability</span>
                <strong>
                  {selected.probability != null
                    ? `${(selected.probability * 100).toFixed(1)}%`
                    : "—"}
                </strong>
              </div>

              <div>
                <RiskBadge level={selected.severity} />

                {selected.isDelayed != null && (
                  <span
                    className={
                      selected.isDelayed
                        ? "prediction-decision delayed"
                        : "prediction-decision on-track"
                    }
                  >
                    {selected.isDelayed
                      ? "Delay likely"
                      : "On track"}
                  </span>
                )}
              </div>
            </div>

            <div className="risk-modal-description">
              <b>Signal</b>
              <p>{selected.description}</p>
            </div>

            {selected.severity === "high" && (
              <div className="risk-next-steps">
                <h3>Recommended next steps</h3>
                <ol>
                  <li>
                    Validate route weather and disruption intelligence.
                  </li>
                  <li>
                    Review alternate service-level or carrier options.
                  </li>
                  <li>
                    Assign the shipment for active monitoring.
                  </li>
                  <li>
                    Prepare proactive customer communication if risk
                    persists.
                  </li>
                </ol>
              </div>
            )}

            <div className="risk-modal-actions">
              <button
                className="secondary-inline"
                onClick={() => setSelected(null)}
              >
                Close
              </button>

              <AsyncButton
                loading={savingId === selected.id}
                loadingText="Saving"
                className="primary"
                disabled={selected.acknowledged}
                onClick={() => acknowledge(selected)}
              >
                {selected.acknowledged
                  ? "Acknowledged"
                  : "Acknowledge alert"}
              </AsyncButton>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
