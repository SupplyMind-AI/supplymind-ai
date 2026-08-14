import { FormEvent, useEffect, useState } from "react";
import {
  BrainCircuit,
  CalendarClock,
  CheckCircle2,
  Play,
  RefreshCcw,
} from "lucide-react";
import { api, safeApi } from "../api";
import {
  Card,
  Header,
  Metric,
  RiskBadge,
  SectionTitle,
} from "../components";

export default function Retraining() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [reason, setReason] = useState(
    "Manual validation of retraining workflow",
  );
  const [running, setRunning] = useState(false);

  async function load() {
    setJobs(await safeApi<any[]>("/retraining", []));
  }

  useEffect(() => {
    void load();
  }, []);

  async function go(event: FormEvent) {
    event.preventDefault();
    setRunning(true);
    try {
      await api("/retraining", {
        method: "POST",
        body: JSON.stringify({ reason }),
      });
      await load();
    } finally {
      setRunning(false);
    }
  }

  const latest = jobs[0];

  return (
    <>
      <Header
        eyebrow="CHAMPION · CHALLENGER"
        title="Retraining Center"
        subtitle="Controlled model-lifecycle simulation with triggers, challenger evaluation and promotion history."
      />

      <div className="metrics four">
        <Metric
          label="Champion Status"
          value="Active"
          tone="success"
          icon={<BrainCircuit size={16} />}
        />
        <Metric
          label="Recent Jobs"
          value={jobs.length}
          icon={<RefreshCcw size={16} />}
        />
        <Metric
          label="Next Evaluation"
          value="Scheduled"
          icon={<CalendarClock size={16} />}
        />
        <Metric
          label="Latest Decision"
          value={latest?.status ?? "Ready"}
          tone={latest?.status === "failed" ? "danger" : "success"}
          icon={<CheckCircle2 size={16} />}
        />
      </div>

      <div className="grid2">
        <Card>
          <SectionTitle
            title="Model lifecycle"
            subtitle="Production retraining workflow"
          />

          <div className="lifecycle">
            {[
              "Validate new labelled batch",
              "Build training dataset",
              "Train candidate models",
              "Evaluate challenger",
              "Compare against champion",
              "Promote only if better",
            ].map((step, index) => (
              <div className="lifecycle-step" key={step}>
                <span>{index + 1}</span>
                <div>
                  <b>{step}</b>
                  <small>
                    {index < 4
                      ? "Automated workflow stage"
                      : "Controlled promotion gate"}
                  </small>
                </div>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <SectionTitle
            title="Run controlled retraining"
            subtitle="V1 honestly simulates new-data arrival using retained holdout data"
          />

          <form className="stack" onSubmit={go}>
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />
            <button className="primary" disabled={running}>
              <Play size={15} />
              {running ? "Queueing…" : "Run retraining workflow"}
            </button>
          </form>

          <div className="policy-box">
            <b>Promotion policy</b>
            <p>
              A challenger is promoted only when it outperforms the
              active champion according to the configured validation
              policy.
            </p>
          </div>
        </Card>
      </div>

      <Card>
        <SectionTitle
          title="Retraining history"
          subtitle="Saved workflow jobs and promotion outcomes"
        />

        <div className="premium-table">
          <div className="premium-table-head four">
            <span>Reason</span>
            <span>Trigger</span>
            <span>Status</span>
            <span>Requested</span>
          </div>
          {jobs.map((job, index) => (
            <div
              className="premium-table-row four"
              key={job.id ?? index}
            >
              <b>{job.reason}</b>
              <span>{job.trigger_type ?? "manual"}</span>
              <RiskBadge
                level={
                  job.status === "failed"
                    ? "high"
                    : job.status === "succeeded"
                      ? "low"
                      : "medium"
                }
              />
              <span>
                {job.requested_at
                  ? new Date(job.requested_at).toLocaleString()
                  : "—"}
              </span>
            </div>
          ))}
          {!jobs.length && (
            <div className="table-empty">
              No retraining jobs recorded yet.
            </div>
          )}
        </div>
      </Card>
    </>
  );
}
