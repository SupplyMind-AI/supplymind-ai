import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  BarChart3,
  Gauge,
  ShieldCheck,
  TrendingUp,
} from "lucide-react";

import { safeApi } from "../api";
import {
  BarChart,
  Card,
  Header,
  Metric,
  MiniTrend,
  SectionTitle,
} from "../components";
import { predictionView } from "../predictionView";

function numberOrNull(...values: unknown[]): number | null {
  for (const value of values) {
    const parsed = Number(value);
    if (value !== null && value !== undefined && Number.isFinite(parsed)) {
      return parsed;
    }
  }
  return null;
}

function metricContainer(champion: any, latest: any) {
  return (
    latest?.metrics ??
    champion?.metrics ??
    champion?.metadata?.test_metrics ??
    champion?.metadata?.validation_metrics ??
    champion?.metadata?.metrics ??
    {}
  );
}

function snapshotMetric(snapshot: any, key: string) {
  return numberOrNull(
    snapshot?.metrics?.[key],
    snapshot?.[key],
  );
}

export default function Monitoring() {
  const [monitoring, setMonitoring] = useState<any>(null);
  const [rawPredictions, setRawPredictions] = useState<any[]>([]);

  useEffect(() => {
    void Promise.all([
      safeApi<any>("/monitoring", {}),
      safeApi<any[]>("/predictions?limit=200", []),
    ]).then(([monitoringResponse, predictionResponse]) => {
      setMonitoring(monitoringResponse);
      setRawPredictions(predictionResponse);
    });
  }, []);

  const champion = monitoring?.champion ?? null;
  const snapshots: any[] = Array.isArray(monitoring?.snapshots)
    ? monitoring.snapshots
    : [];

  const latest = snapshots[0] ?? null;
  const metrics = metricContainer(champion, latest);

  const accuracy = numberOrNull(metrics.accuracy);
  const precision = numberOrNull(metrics.precision);
  const recall = numberOrNull(metrics.recall);
  const f1 = numberOrNull(metrics.f1);
  const rocAuc = numberOrNull(metrics.roc_auc, metrics.rocAuc);

  const predictions = useMemo(
    () => rawPredictions.map(predictionView),
    [rawPredictions],
  );

  const distribution = useMemo(() => {
    const counts = { high: 0, medium: 0, low: 0 };

    predictions.forEach((prediction) => {
      counts[prediction.riskLevel] += 1;
    });

    return counts;
  }, [predictions]);

  const totalPredictions = predictions.length;
  const delayedPredictions = predictions.filter(
    (prediction) => prediction.isDelayed,
  ).length;

  const distributionRows = [
    {
      label: "High risk",
      value: totalPredictions
        ? (distribution.high / totalPredictions) * 100
        : 0,
      note: `${distribution.high} predictions`,
    },
    {
      label: "Medium risk",
      value: totalPredictions
        ? (distribution.medium / totalPredictions) * 100
        : 0,
      note: `${distribution.medium} predictions`,
    },
    {
      label: "Low risk",
      value: totalPredictions
        ? (distribution.low / totalPredictions) * 100
        : 0,
      note: `${distribution.low} predictions`,
    },
  ];

  const f1History = snapshots
    .map((snapshot) => snapshotMetric(snapshot, "f1"))
    .filter((value): value is number => value != null)
    .reverse()
    .map((value) => value * 100);

  const historyLabels = snapshots
    .filter((snapshot) => snapshotMetric(snapshot, "f1") != null)
    .reverse()
    .map((snapshot, index) => {
      const rawDate =
        snapshot.evaluated_at ??
        snapshot.created_at ??
        snapshot.computed_at;

      return rawDate
        ? new Date(rawDate).toLocaleDateString()
        : `Snapshot ${index + 1}`;
    });

  const driftScore = numberOrNull(
    latest?.drift_score,
    latest?.psi,
    latest?.population_stability_index,
    latest?.metrics?.drift_score,
    latest?.metrics?.psi,
  );

  const sampleCount = numberOrNull(
    latest?.sample_count,
    latest?.prediction_count,
    latest?.metrics?.sample_count,
  );

  const evaluatedAt =
    latest?.evaluated_at ??
    latest?.created_at ??
    latest?.computed_at ??
    null;

  const modelName =
    champion?.model_name ??
    champion?.name ??
    champion?.metadata?.model_name ??
    "Champion not registered";

  const modelVersion =
    champion?.version ??
    champion?.model_version ??
    champion?.metadata?.model_version ??
    "—";

  const championStatus = champion ? "Registered" : "Unavailable";

  return (
    <>
      <Header
        eyebrow="MLOPS"
        title="Model Monitoring"
        subtitle="Reliability, performance, prediction distribution and drift signals for the deployed champion."
      />

      <Card className="monitoring-champion-strip compact-card">
        <div className="champion-strip-copy">
          <span>ACTIVE CHAMPION</span>
          <h2>{modelName}</h2>
          <p>
            Version {modelVersion} · Registry {championStatus.toLowerCase()}
          </p>
        </div>

        <div className="champion-strip-stats">
          <div>
            <span>Live predictions</span>
            <b>{totalPredictions}</b>
          </div>
          <div>
            <span>Delay likely</span>
            <b>{delayedPredictions}</b>
          </div>
          <div>
            <span>Last evaluated</span>
            <b>
              {evaluatedAt
                ? new Date(evaluatedAt).toLocaleString()
                : "No snapshot"}
            </b>
          </div>
        </div>
      </Card>

      <div className="metrics five compact-metrics">
        <Metric
          label="Accuracy"
          value={
            accuracy != null
              ? `${(accuracy * 100).toFixed(1)}%`
              : "—"
          }
          delta="Champion evaluation"
          icon={<Gauge size={16} />}
        />
        <Metric
          label="Precision"
          value={
            precision != null
              ? `${(precision * 100).toFixed(1)}%`
              : "—"
          }
          delta="Champion evaluation"
          tone="success"
          icon={<ShieldCheck size={16} />}
        />
        <Metric
          label="Recall"
          value={
            recall != null
              ? `${(recall * 100).toFixed(1)}%`
              : "—"
          }
          delta="Champion evaluation"
          icon={<TrendingUp size={16} />}
        />
        <Metric
          label="F1"
          value={
            f1 != null
              ? `${(f1 * 100).toFixed(1)}%`
              : "—"
          }
          delta="Champion evaluation"
          icon={<Activity size={16} />}
        />
        <Metric
          label="ROC-AUC"
          value={rocAuc != null ? rocAuc.toFixed(3) : "—"}
          delta="Champion evaluation"
          icon={<BarChart3 size={16} />}
        />
      </div>

      <div className="grid2 monitoring-grid">
        <Card className="compact-card">
          <SectionTitle
            title="Performance"
            subtitle={
              f1History.length
                ? `${f1History.length} real monitoring snapshots`
                : "No monitoring snapshots recorded yet"
            }
          />

          {f1History.length ? (
            <div className="monitoring-chart-v2">
              <div className="monitoring-current">
                <span>Latest F1</span>
                <strong>
                  {f1 != null
                    ? `${(f1 * 100).toFixed(1)}%`
                    : `${f1History[f1History.length - 1].toFixed(1)}%`}
                </strong>
              </div>

              <MiniTrend
                values={f1History}
                labels={historyLabels}
              />
            </div>
          ) : (
            <div className="monitoring-empty">
              <Activity size={27} />
              <b>No performance history yet</b>
              <p>
                Metrics will appear here after monitoring snapshots are
                generated for the registered champion.
              </p>
            </div>
          )}
        </Card>

        <Card className="compact-card">
          <SectionTitle
            title="Prediction distribution"
            subtitle={`${totalPredictions} live persisted predictions`}
          />

          {totalPredictions ? (
            <BarChart rows={distributionRows} />
          ) : (
            <div className="monitoring-empty">
              <BarChart3 size={27} />
              <b>No prediction distribution yet</b>
              <p>Score shipments to populate live distribution signals.</p>
            </div>
          )}
        </Card>

        <Card className="compact-card">
          <SectionTitle
            title="Drift signals"
            subtitle="Latest production monitoring snapshot"
          />

          <div className="monitoring-signal-list">
            <div>
              <span>Drift / PSI score</span>
              <b>
                {driftScore != null
                  ? driftScore.toFixed(3)
                  : "Not measured"}
              </b>
            </div>
            <div>
              <span>Snapshot sample count</span>
              <b>
                {sampleCount != null
                  ? Math.round(sampleCount)
                  : "—"}
              </b>
            </div>
            <div>
              <span>Snapshot availability</span>
              <b className={latest ? "signal-ok" : "signal-neutral"}>
                {latest ? "Available" : "Pending"}
              </b>
            </div>
          </div>

          {!latest && (
            <p className="monitoring-note">
              No drift value is fabricated. The screen will display the
              persisted PSI/drift score once the monitoring pipeline creates
              a snapshot.
            </p>
          )}
        </Card>

        <Card className="compact-card">
          <SectionTitle
            title="Reliability"
            subtitle="Current deployment evidence"
          />

          <div className="monitoring-signal-list">
            <div>
              <span>Champion registry</span>
              <b className={champion ? "signal-ok" : "signal-warn"}>
                {championStatus}
              </b>
            </div>
            <div>
              <span>Evaluation metrics</span>
              <b className={f1 != null ? "signal-ok" : "signal-neutral"}>
                {f1 != null ? "Available" : "Not available"}
              </b>
            </div>
            <div>
              <span>Live prediction feed</span>
              <b
                className={
                  totalPredictions ? "signal-ok" : "signal-neutral"
                }
              >
                {totalPredictions ? "Active" : "No data"}
              </b>
            </div>
          </div>

          <p className="monitoring-note">
            Evaluation metrics come from the registered champion metadata or
            monitoring snapshot. Prediction distribution comes from the live
            persisted predictions — nothing on this screen is hardcoded.
          </p>
        </Card>
      </div>
    </>
  );
}
