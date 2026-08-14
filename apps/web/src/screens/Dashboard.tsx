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
import { predictionView } from "../predictionView";

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
  const [rawPredictions, setRawPredictions] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;

    async function load() {
      const [predictionResponse, eventResponse] = await Promise.all([
        safeApi<any[]>("/predictions", []),
        safeApi<any[]>("/events", []),
      ]);

      if (!alive) return;
      setRawPredictions(predictionResponse);
      setEvents(eventResponse);
      setLoading(false);
    }

    void load();
    return () => {
      alive = false;
    };
  }, []);

  const predictions = useMemo(
    () => rawPredictions.map(predictionView),
    [rawPredictions],
  );

  const totalShipments = predictions.length;
  const delayed = predictions.filter((x) => x.isDelayed).length;
  const highRisk = predictions.filter((x) => x.riskLevel === "high").length;
  const avgRisk = predictions.length
    ? predictions.reduce((sum, x) => sum + x.probability, 0) /
      predictions.length
    : 0;
  const onTimeRate = totalShipments
    ? ((totalShipments - delayed) / totalShipments) * 100
    : 0;

  const riskCounts = useMemo(
    () =>
      predictions.reduce(
        (acc, item) => {
          acc[item.riskLevel] += 1;
          return acc;
        },
        { high: 0, medium: 0, low: 0 },
      ),
    [predictions],
  );

  const trend = predictions.slice(-14).map((item) => item.probability * 100);
  const topPredictions = [...predictions]
    .sort((a, b) => b.probability - a.probability)
    .slice(0, 5);

  const modeGroups = useMemo(() => {
    const grouped = new Map<string, number[]>();

    predictions.forEach((prediction) => {
      if (!prediction.shippingMode) return;
      const values = grouped.get(prediction.shippingMode) ?? [];
      values.push(prediction.probability * 100);
      grouped.set(prediction.shippingMode, values);
    });

    return [...grouped.entries()]
      .map(([label, values]) => ({
        label,
        value:
          values.reduce((sum, value) => sum + value, 0) /
          Math.max(values.length, 1),
        note: `${values.length} shipment${values.length === 1 ? "" : "s"}`,
      }))
      .sort((a, b) => b.value - a.value);
  }, [predictions]);

  const latestEvents = [...events]
    .sort((a, b) => Number(b.severity ?? 0) - Number(a.severity ?? 0))
    .slice(0, 4);

  return (
    <>
      <Header
        eyebrow="LIVE SUPPLY-CHAIN INTELLIGENCE"
        title="Command Center"
        subtitle="One view across shipment risk, disruptions, model health and AI recommendations."
        action={
          <button className="primary" onClick={() => onNavigate("assistant")}>
            <Sparkles size={16} />
            Investigate with AI
          </button>
        }
      />

      <div className="metrics four">
        <Metric
          label="Total Shipments"
          value={loading ? "—" : totalShipments}
          delta="Scored operational records"
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
          value={loading ? "—" : `${onTimeRate.toFixed(1)}%`}
          delta="Predicted portfolio outcome"
          tone="success"
          icon={<PackageCheck size={18} />}
        />
        <Metric
          label="Average Risk"
          value={loading ? "—" : `${(avgRisk * 100).toFixed(1)}%`}
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
              <strong>{(avgRisk * 100).toFixed(1)}%</strong>
              <small>Updated from persisted predictions</small>
            </div>
            <MiniTrend
              values={trend.length ? trend : [32, 37, 31, 45, 41, 51, 48, 57]}
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
            subtitle="Hover or click a risk band to inspect its value"
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
            description="Inspect high-probability records together with route context and predicted outcome."
          />
          <InsightRow
            tone={latestEvents.length ? "warning" : "success"}
            title={`${latestEvents.length} priority disruption signals`}
            description="External intelligence can be investigated by region and severity."
          />
          <InsightRow
            title="Champion model is active"
            description="Model Monitoring and Retraining Center expose model health and challenger workflow."
          />
        </Card>
      </div>

      <div className="grid2 dashboard-chart-row">
        <Card>
          <SectionTitle
            title="Risk by shipping mode"
            subtitle="Average delay probability by actual service level"
          />
          {modeGroups.length ? (
            <BarChart rows={modeGroups} />
          ) : (
            <div className="premium-empty-state compact">
              <b>Shipping-mode context is unavailable</b>
              <p>Score shipments with route context to populate this chart.</p>
            </div>
          )}
        </Card>

        <Card>
          <SectionTitle
            title="Highest-risk shipments"
            subtitle="Prioritized by delay probability"
            action={
              <button className="text-button" onClick={() => onNavigate("predictions")}>
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
              <span>Prediction</span>
            </div>

            {topPredictions.length ? (
              topPredictions.map((item) => (
                <div className="premium-table-row five" key={item.id || item.shipmentId}>
                  <b>{item.shipmentId}</b>
                  <span>
                    {item.origin ?? "—"} → {item.destination ?? "—"}
                  </span>
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
              ))
            ) : (
              <div className="table-empty">Score a parcel to populate shipment intelligence.</div>
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
              <button className="text-button" onClick={() => onNavigate("events")}>
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
                      {[event.region, event.country].filter(Boolean).join(", ") || "Global"}
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
              <div className="table-empty">No event intelligence loaded yet.</div>
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
