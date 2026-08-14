import { useEffect, useMemo, useState } from "react";
import {
  AlertTriangle,
  FileBarChart2,
  Sparkles,
  TrendingUp,
} from "lucide-react";
import { safeApi } from "../api";
import {
  Card,
  Header,
  InsightRow,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";

export default function Reports() {
  const [predictions, setPredictions] = useState<any[]>([]);
  const [events, setEvents] = useState<any[]>([]);

  useEffect(() => {
    void Promise.all([
      safeApi<any[]>("/predictions", []),
      safeApi<any[]>("/events", []),
    ]).then(([predictionData, eventData]) => {
      setPredictions(predictionData);
      setEvents(eventData);
    });
  }, []);

  const normalized = useMemo(
    () =>
      predictions.map((item) => ({
        ...item,
        probability: Number(
          item.delay_probability ?? item.probability ?? 0,
        ),
      })),
    [predictions],
  );

  const high = normalized.filter((x) => x.probability >= 0.7);
  const avg =
    normalized.length
      ? normalized.reduce((sum, x) => sum + x.probability, 0) /
        normalized.length
      : 0;

  return (
    <>
      <Header
        eyebrow="EXECUTIVE INTELLIGENCE"
        title="Operational Brief"
        subtitle="Presentation-ready summary of shipment exposure, external risk and recommended focus."
        action={
          <button className="secondary-inline">
            <FileBarChart2 size={15} />
            Executive view
          </button>
        }
      />

      <div className="metrics four">
        <Metric label="Scored shipments" value={normalized.length} />
        <Metric
          label="High-risk exposure"
          value={high.length}
          tone="danger"
          icon={<AlertTriangle size={16} />}
        />
        <Metric
          label="Average risk"
          value={`${(avg * 100).toFixed(1)}%`}
          tone="warning"
          icon={<TrendingUp size={16} />}
        />
        <Metric
          label="External signals"
          value={events.length}
          icon={<Sparkles size={16} />}
        />
      </div>

      <div className="grid2">
        <Card>
          <SectionTitle
            title="Executive summary"
            subtitle="Current operational posture"
          />
          <InsightRow
            tone={high.length ? "danger" : "success"}
            title={
              high.length
                ? `${high.length} shipments require priority review`
                : "No critical shipment cluster detected"
            }
            description="High-risk exposure is calculated from persisted champion predictions."
          />
          <InsightRow
            tone={events.length ? "warning" : "success"}
            title={`${events.length} external disruption signals are available`}
            description="Use Event Monitor and the AI Assistant to investigate relevance to specific routes."
          />
          <InsightRow
            title="Champion–challenger lifecycle is operational"
            description="Model Monitoring and Retraining Center expose the model lifecycle and promotion policy."
          />
        </Card>

        <Card>
          <SectionTitle
            title="Priority shipments"
            subtitle="Highest current probability"
          />
          <div className="event-stack">
            {[...normalized]
              .sort((a, b) => b.probability - a.probability)
              .slice(0, 5)
              .map((item, index) => (
                <div className="event-stack-row" key={item.id ?? index}>
                  <div className="event-severity">
                    {(item.probability * 100).toFixed(0)}
                  </div>
                  <div>
                    <b>
                      {item.external_id ??
                        item.shipment_id ??
                        `Shipment ${index + 1}`}
                    </b>
                    <p>
                      {item.customer_city ?? "Origin"} →{" "}
                      {item.order_city ?? "Destination"}
                    </p>
                  </div>
                  <RiskBadge
                    level={
                      item.probability >= 0.7
                        ? "high"
                        : item.probability >= 0.4
                          ? "medium"
                          : "low"
                    }
                  />
                </div>
              ))}
          </div>
        </Card>
      </div>
    </>
  );
}
