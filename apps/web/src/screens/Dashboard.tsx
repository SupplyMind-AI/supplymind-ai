import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BrainCircuit,
  PackageCheck,
  PackageSearch,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import { safeApi } from "../api";
import {
  BarChart,
  Card,
  DonutChart,
  Header,
  InsightRow,
  Metric,
  MiniTrend,
  RiskBadge,
  SectionTitle,
} from "../components";

type Screen =
  | "dashboard"
  | "assistant"
  | "prediction"
  | "predictions"
  | "alerts"
  | "events"
  | "search"
  | "reports"
  | "monitoring"
  | "retraining"
  | "settings";

export default function Dashboard({
  onNavigate,
}: {
  onNavigate: (screen: Screen) => void;
}) {
  const [summary, setSummary] = useState<any>(null);
  const [predictions, setPredictions] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;

    async function load() {
      const [dashboard, pred, evt] = await Promise.all([
        safeApi<any>("/dashboard", {}),
        safeApi<any[]>("/predictions", []),
        safeApi<any[]>("/events", []),
      ]);

      if (!alive) return;
      setSummary(dashboard);
      setPredictions(pred);
      setEvents(evt);
      setLoading(false);
    }

    void load();
    return () => {
      alive = false;
    };
  }, []);

  const totalShipments =
    summary?.total_shipments ??
    summary?.shipments ??
    predictions.length;

  const delayed =
    summary?.predicted_delays ??
    summary?.delayed_shipments ??
    predictions.filter((x) => Boolean(x.is_delayed ?? x.predicted_delay))
      .length;

  const highRisk =
    summary?.high_risk_shipments ??
    predictions.filter(
      (x) =>
        String(x.risk_level ?? "").toLowerCase() === "high" ||
        Number(x.delay_probability ?? x.probability ?? 0) >= 0.7,
    ).length;

  const avgRisk =
    summary?.average_delay_score ??
    (predictions.length
      ? predictions.reduce(
          (sum, x) =>
            sum + Number(x.delay_probability ?? x.probability ?? 0),
          0,
        ) / predictions.length
      : 0);

  const onTimeRate =
    summary?.on_time_rate ??
    (totalShipments
      ? ((totalShipments - delayed) / totalShipments) * 100
      : 0);

  const riskCounts = useMemo(() => {
    const result = { high: 0, medium: 0, low: 0 };
    for (const p of predictions) {
      const probability = Number(
        p.delay_probability ?? p.probability ?? p.risk_score ?? 0,
      );
      const level =
        String(p.risk_level ?? "").toLowerCase() ||
        (probability >= 0.7
          ? "high"
          : probability >= 0.4
            ? "medium"
            : "low");

      if (level in result) {
        result[level as keyof typeof result] += 1;
      }
    }
    return result;
  }, [predictions]);

  const trend = predictions
    .slice(-14)
    .map((p) => Number(p.delay_probability ?? p.probability ?? 0) * 100);

  const topPredictions = [...predictions]
    .sort(
      (a, b) =>
        Number(b.delay_probability ?? b.probability ?? 0) -
        Number(a.delay_probability ?? a.probability ?? 0),
    )
    .slice(0, 5);

  const latestEvents = [...events]
    .sort(
      (a, b) =>
        Number(b.severity ?? 0) - Number(a.severity ?? 0),
    )
    .slice(0, 4);

  const modeGroups = useMemo(() => {
    const grouped: Record<string, number[]> = {};

    for (const prediction of predictions) {
      const mode = prediction.shipping_mode ?? "Unknown";
      const probability =
        Number(prediction.delay_probability ?? prediction.probability ?? 0) *
        100;

      grouped[mode] ??= [];
      grouped[mode].push(probability);
    }

    const rows = Object.entries(grouped)
      .map(([label, values]) => ({
        label,
        value:
          values.reduce((sum, value) => sum + value, 0) /
          Math.max(values.length, 1),
        note: `${values.length} shipment${values.length === 1 ? "" : "s"}`,
      }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 5);

    return rows.length
      ? rows
      : [
          { label: "Standard Class", value: 64, note: "Typical demo exposure" },
          { label: "Second Class", value: 55, note: "Typical demo exposure" },
          { label: "First Class", value: 42, note: "Typical demo exposure" },
          { label: "Same Day", value: 31, note: "Typical demo exposure" },
        ];
  }, [predictions]);

  return (
    <>
      <Header
        eyebrow="LIVE SUPPLY-CHAIN INTELLIGENCE"
        title="Command Center"
        subtitle="One view across shipment risk, disruptions, model health and AI recommendations."
        action={
          <button
            className="primary"
            onClick={() => onNavigate("assistant")}
          >
            <Sparkles size={16} />
            Investigate with AI
          </button>
        }
      />

      <div className="metrics four">
        <Metric
          label="Total Shipments"
          value={loading ? "—" : totalShipments}
          delta="Operational records"
          icon={<PackageSearch size={18} />}
        />
        <Metric
          label="Predicted Delays"
          value={loading ? "—" : delayed}
          delta={`${highRisk} high-risk`}
          tone="danger"
          icon={<AlertTriangle size={18} />}
        />
        <Metric
          label="On-time Rate"
          value={loading ? "—" : `${Number(onTimeRate).toFixed(1)}%`}
          delta="Current portfolio"
          tone="success"
          icon={<PackageCheck size={18} />}
        />
        <Metric
          label="Average Risk"
          value={loading ? "—" : `${(Number(avgRisk) * 100).toFixed(1)}%`}
          delta="Champion score"
          tone="warning"
          icon={<Activity size={18} />}
        />
      </div>

      <div className="dashboard-hero-grid">
        <Card className="trend-card">
          <SectionTitle
            title="Delay Risk Trend"
            subtitle="Latest scored shipments"
            action={<span className="live-chip">LIVE</span>}
          />
          <div className="trend-big-v2">
            <div className="trend-number">
              <span>Average predicted risk</span>
              <strong>{(Number(avgRisk) * 100).toFixed(1)}%</strong>
              <small>Updated from persisted predictions</small>
            </div>
            <MiniTrend
              values={
                trend.length ? trend : [32, 37, 31, 45, 41, 51, 48, 57]
              }
            />
          </div>
          <div className="trend-footer">
            <span>Low 0–39%</span>
            <span>Medium 40–69%</span>
            <span>High 70%+</span>
          </div>
        </Card>

        <Card>
          <SectionTitle
            title="Risk Distribution"
            subtitle="Portfolio exposure"
          />
          <DonutChart
            centerLabel="scored"
            centerValue={predictions.length}
            segments={[
              { label: "High", value: riskCounts.high, tone: "high" },
              { label: "Medium", value: riskCounts.medium, tone: "medium" },
              { label: "Low", value: riskCounts.low, tone: "low" },
            ]}
          />
        </Card>

        <Card className="ai-brief-card">
          <SectionTitle
            title="AI Operations Brief"
            subtitle="What deserves attention now"
            action={<BrainCircuit size={19} />}
          />
          <InsightRow
            tone={highRisk ? "danger" : "success"}
            title={
              highRisk
                ? `${highRisk} high-risk shipments need review`
                : "No critical shipment cluster detected"
            }
            description="Open Shipment Intelligence to inspect the highest probability records and supporting evidence."
          />
          <InsightRow
            tone={latestEvents.length ? "warning" : "success"}
            title={`${latestEvents.length} priority disruption signals`}
            description="External intelligence is normalized from the event feed and can be investigated by region and severity."
          />
          <InsightRow
            title="Champion model is active"
            description="Model Monitoring and Retraining Center expose model health, challenger jobs and promotion history."
          />
        </Card>
      </div>

      <div className="grid2 dashboard-chart-row">
        <Card>
          <SectionTitle
            title="Risk by shipping mode"
            subtitle="Average delay probability by service level"
          />
          <BarChart rows={modeGroups} />
        </Card>

        <Card>
          <SectionTitle
            title="Highest-risk shipments"
            subtitle="Prioritized by delay probability"
            action={
              <button
                className="text-button"
                onClick={() => onNavigate("predictions")}
              >
                View intelligence →
              </button>
            }
          />
          <div className="premium-table">
            <div className="premium-table-head five">
              <span>Shipment</span>
              <span>Route</span>
              <span>Risk</span>
              <span>Score</span>
              <span>Status</span>
            </div>

            {topPredictions.length ? (
              topPredictions.map((p, index) => {
                const probability = Number(
                  p.delay_probability ?? p.probability ?? 0,
                );
                const level =
                  p.risk_level ??
                  (probability >= 0.7
                    ? "high"
                    : probability >= 0.4
                      ? "medium"
                      : "low");

                return (
                  <div className="premium-table-row five" key={p.id ?? index}>
                    <b>
                      {p.external_id ??
                        p.shipment_id ??
                        p.id ??
                        `Shipment ${index + 1}`}
                    </b>
                    <span>
                      {p.origin_city ??
                        p.customer_city ??
                        "Origin"}{" "}
                      →{" "}
                      {p.destination_city ??
                        p.order_city ??
                        "Destination"}
                    </span>
                    <RiskBadge level={level} />
                    <strong>{(probability * 100).toFixed(0)}%</strong>
                    <span>
                      {p.is_delayed ?? p.predicted_delay
                        ? "Delay"
                        : "On track"}
                    </span>
                  </div>
                );
              })
            ) : (
              <div className="table-empty">
                Score a parcel to populate shipment intelligence.
              </div>
            )}
          </div>
        </Card>
      </div>

      <div className="grid2">
        <Card>
          <SectionTitle
            title="Disruption Radar"
            subtitle="Highest-severity external events"
            action={
              <button
                className="text-button"
                onClick={() => onNavigate("events")}
              >
                Open map →
              </button>
            }
          />
          <div className="event-stack">
            {latestEvents.length ? (
              latestEvents.map((event, index) => (
                <div className="event-stack-row" key={event.id ?? index}>
                  <div className="event-severity">
                    {Number(event.severity ?? 0).toFixed(1)}
                  </div>
                  <div>
                    <b>{event.title ?? "Supply-chain event"}</b>
                    <p>
                      {[event.region, event.country]
                        .filter(Boolean)
                        .join(", ") || "Global"}
                    </p>
                  </div>
                  <RiskBadge
                    level={
                      Number(event.severity ?? 0) >= 0.7
                        ? "high"
                        : Number(event.severity ?? 0) >= 0.4
                          ? "medium"
                          : "low"
                    }
                  />
                </div>
              ))
            ) : (
              <div className="table-empty">
                No event intelligence loaded yet.
              </div>
            )}
          </div>
        </Card>

        <Card className="system-strip-card">
          <SectionTitle
            title="Production architecture"
            subtitle="Operational V1 deployment topology"
            action={<ShieldCheck size={19} />}
          />
          <div className="architecture-mini-grid">
            <span>React / Vercel</span>
            <span>FastAPI / Render</span>
            <span>PostgreSQL</span>
            <span>Pinecone</span>
            <span>LangGraph</span>
            <span>External Intelligence</span>
          </div>
        </Card>
      </div>
    </>
  );
}
