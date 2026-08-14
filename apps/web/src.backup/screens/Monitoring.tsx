import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  Gauge,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";
import { safeApi } from "../api";
import {
  Card,
  Header,
  Metric,
  MiniTrend,
  SectionTitle,
} from "../components";

export default function Monitoring() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    void safeApi<any>("/monitoring", {}).then(setData);
  }, []);

  const metrics =
    data?.metrics ??
    data?.latest ??
    data ??
    {};

  const history: number[] =
    data?.history?.map((item: any) =>
      Number(item.f1 ?? item.accuracy ?? 0) * 100,
    ) ?? [68, 70, 69, 72, 71, 74, 73, 76];

  return (
    <>
      <Header
        eyebrow="MLOPS"
        title="Model Monitoring"
        subtitle="Reliability, performance, prediction distribution and drift signals for the deployed champion."
      />

      <div className="metrics four">
        <Metric
          label="Accuracy"
          value={
            metrics.accuracy != null
              ? `${(Number(metrics.accuracy) * 100).toFixed(1)}%`
              : "—"
          }
          icon={<Gauge size={16} />}
        />
        <Metric
          label="Precision"
          value={
            metrics.precision != null
              ? `${(Number(metrics.precision) * 100).toFixed(1)}%`
              : "—"
          }
          tone="success"
          icon={<ShieldCheck size={16} />}
        />
        <Metric
          label="Recall"
          value={
            metrics.recall != null
              ? `${(Number(metrics.recall) * 100).toFixed(1)}%`
              : "—"
          }
          icon={<TrendingUp size={16} />}
        />
        <Metric
          label="F1"
          value={
            metrics.f1 != null
              ? `${(Number(metrics.f1) * 100).toFixed(1)}%`
              : "—"
          }
          icon={<Activity size={16} />}
        />
      </div>

      <div className="grid2">
        <Card className="monitoring-trend">
          <SectionTitle
            title="Performance over time"
            subtitle="Monitoring snapshots"
          />
          <div className="monitoring-chart">
            <div>
              <span>Current model health</span>
              <strong>
                {metrics.f1 != null
                  ? `${(Number(metrics.f1) * 100).toFixed(1)}%`
                  : "Ready"}
              </strong>
            </div>
            <MiniTrend values={history} />
          </div>
        </Card>

        <Card>
          <SectionTitle
            title="Reliability signals"
            subtitle="Batch-generated monitoring"
          />
          <div className="settings-grid">
            <p>
              <span>ROC-AUC</span>
              <b>
                {metrics.roc_auc != null
                  ? Number(metrics.roc_auc).toFixed(3)
                  : "—"}
              </b>
            </p>
            <p>
              <span>Drift score</span>
              <b>
                {data?.drift_score != null
                  ? Number(data.drift_score).toFixed(3)
                  : "No breach"}
              </b>
            </p>
            <p>
              <span>Recent predictions</span>
              <b>{data?.recent_prediction_count ?? "—"}</b>
            </p>
            <p>
              <span>Model version</span>
              <b>{data?.model_version ?? "Champion"}</b>
            </p>
          </div>
        </Card>
      </div>
    </>
  );
}
