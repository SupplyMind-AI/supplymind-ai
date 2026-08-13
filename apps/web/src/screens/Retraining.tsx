import {
  FormEvent,
  useCallback,
  useEffect,
  useState,
} from "react";

import { api } from "../api";
import { Card, Header, RiskBadge } from "../components";

type RetrainingJob = {
  id: string;
  reason: string;
  trigger_type?: string | null;
  status: string;
  requested_at?: string | null;
};

export default function Retraining() {
  const [jobs, setJobs] = useState<RetrainingJob[]>([]);
  const [reason, setReason] = useState(
    "Manual validation of retraining workflow",
  );
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      const data = await api<RetrainingJob[]>("/retraining");
      setJobs(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to load retraining jobs.",
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedReason = reason.trim();
    if (!trimmedReason) {
      setError("Please provide a reason for the retraining request.");
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      await api<unknown>("/retraining", {
        method: "POST",
        body: JSON.stringify({ reason: trimmedReason }),
      });
      await load();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to queue the retraining job.",
      );
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <Header
        title="Retraining Center"
        subtitle="Review model retraining jobs and queue a controlled manual run."
      />

      {error && (
        <Card>
          <p role="alert">{error}</p>
        </Card>
      )}

      <div className="grid2">
        <Card>
          <h2>Manual retraining</h2>

          <form className="stack" onSubmit={submit}>
            <label htmlFor="retraining-reason">Reason</label>

            <textarea
              id="retraining-reason"
              value={reason}
              onChange={(event) => setReason(event.target.value)}
              rows={5}
              disabled={submitting}
            />

            <button
              className="primary"
              type="submit"
              disabled={submitting}
            >
              {submitting ? "Queuing…" : "Queue retraining job"}
            </button>
          </form>
        </Card>

        <Card>
          <h2>Automation policy</h2>
          <p className="policy">
            Retraining remains asynchronous. FastAPI only queues work; training
            is executed by the dedicated training workflow. This keeps
            long-running model training outside HTTP request handling.
          </p>
        </Card>
      </div>

      <Card>
        <div className="table header-row">
          <div>Reason</div>
          <div>Trigger</div>
          <div>Status</div>
          <div>Requested</div>
        </div>

        {loading && <div className="empty-state">Loading retraining jobs…</div>}

        {!loading && jobs.length === 0 && (
          <div className="empty-state">No retraining jobs have been queued.</div>
        )}

        {jobs.map((job) => {
          const riskLevel =
            job.status === "failed"
              ? "high"
              : job.status === "succeeded" || job.status === "completed"
                ? "low"
                : "medium";

          return (
            <div className="retrain-row" key={job.id}>
              <div>{job.reason}</div>
              <div>{job.trigger_type || "manual"}</div>
              <div>
                <RiskBadge level={riskLevel} /> {job.status}
              </div>
              <div>
                {job.requested_at
                  ? new Date(job.requested_at).toLocaleString()
                  : "—"}
              </div>
            </div>
          );
        })}
      </Card>
    </>
  );
}
