import { FormEvent, useEffect, useState } from "react";
import {
  BrainCircuit,
  CalendarClock,
  CheckCircle2,
  Play,
  RefreshCcw,
  Sparkles,
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

export default function Retraining() {
  const [jobs, setJobs] = useState<any[]>([]);
  const [reason, setReason] = useState(
    "Manual validation of retraining workflow",
  );
  const [running, setRunning] = useState(false);
  const [queuedJobId, setQueuedJobId] = useState<string | null>(null);
  const [notice, setNotice] = useState("");

  async function load() {
    setJobs(await safeApi<any[]>("/retraining", []));
  }

  useEffect(() => {
    void load();
  }, []);

  async function go(event: FormEvent) {
    event.preventDefault();

    if (!reason.trim() || running) return;

    setRunning(true);
    setNotice("");

    try {
      const created = await api<any>("/retraining", {
        method: "POST",
        body: JSON.stringify({ reason: reason.trim() }),
      });

      setQueuedJobId(created?.id ? String(created.id) : null);
      setNotice(
        "Retraining request queued successfully. The job is persisted and waiting for the training worker/workflow to start.",
      );

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

      <div className="metrics four compact-metrics">
        <Metric
          label="Queue status"
          value={latest?.status ?? "Ready"}
          tone={
            latest?.status === "failed"
              ? "danger"
              : latest?.status === "queued"
                ? "warning"
                : "success"
          }
          icon={<BrainCircuit size={16} />}
        />
        <Metric
          label="Recent jobs"
          value={jobs.length}
          icon={<RefreshCcw size={16} />}
        />
        <Metric
          label="Next evaluation"
          value="Scheduled"
          icon={<CalendarClock size={16} />}
        />
        <Metric
          label="Latest request"
          value={latest ? "Recorded" : "Ready"}
          tone="success"
          icon={<CheckCircle2 size={16} />}
        />
      </div>

      <div className="grid2">
        <Card className="compact-card">
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

        <Card className="compact-card">
          <SectionTitle
            title="Queue controlled retraining"
            subtitle="V1 records the request; a training worker advances queued jobs"
          />

          <form className="stack" onSubmit={go}>
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
            />

            <AsyncButton
              loading={running}
              loadingText="Queuing retraining job"
              className="primary"
              type="submit"
            >
              <Play size={15} />
              Queue retraining job
            </AsyncButton>
          </form>

          {notice && (
            <div className="retraining-success">
              <Sparkles size={16} />
              <div>
                <b>Job queued</b>
                <p>{notice}</p>
              </div>
            </div>
          )}

          <div className="policy-box">
            <b>What “queued” means</b>
            <p>
              The API has persisted the retraining request. It is not yet a
              completed model training run. A worker or training workflow must
              set started_at, run challenger training/evaluation, then update
              the job outcome.
            </p>
          </div>
        </Card>
      </div>

      <Card className="compact-card">
        <SectionTitle
          title="Retraining history"
          subtitle="Saved workflow jobs and lifecycle state"
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
              className={`premium-table-row four retraining-job-row ${
                String(job.id) === queuedJobId ? "just-queued" : ""
              }`}
              key={job.id ?? index}
            >
              <div>
                <b>{job.reason}</b>
                {String(job.id) === queuedJobId && (
                  <small>Newly queued</small>
                )}
              </div>
              <span>{job.trigger_type ?? "manual"}</span>
              <RiskBadge
                level={
                  job.status === "failed"
                    ? "high"
                    : job.status === "succeeded" ||
                        job.status === "completed"
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
