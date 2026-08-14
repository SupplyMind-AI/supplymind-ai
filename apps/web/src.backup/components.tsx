import type { ReactNode } from "react";
import { motion } from "framer-motion";
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  CheckCircle2,
  ChevronRight,
  Clock3,
  Sparkles,
} from "lucide-react";

export function Header({
  title,
  subtitle,
  action,
  eyebrow,
}: {
  title: string;
  subtitle: string;
  action?: ReactNode;
  eyebrow?: string;
}) {
  return (
    <header className="header">
      <div>
        {eyebrow && <div className="eyebrow">{eyebrow}</div>}
        <h1>{title}</h1>
        <p>{subtitle}</p>
      </div>
      {action}
    </header>
  );
}

export function Card({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <motion.section
      className={`card ${className}`}
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.28 }}
    >
      {children}
    </motion.section>
  );
}

export function Metric({
  label,
  value,
  delta,
  icon,
  tone = "default",
}: {
  label: string;
  value: ReactNode;
  delta?: string;
  icon?: ReactNode;
  tone?: "default" | "danger" | "warning" | "success";
}) {
  return (
    <Card className={`metric metric-${tone}`}>
      <div className="metric-top">
        <span>{label}</span>
        {icon && <div className="metric-icon">{icon}</div>}
      </div>
      <strong>{value}</strong>
      {delta && <small>{delta}</small>}
    </Card>
  );
}

export function RiskBadge({ level }: { level: string }) {
  const normalized = String(level || "low").toLowerCase();
  return <span className={`badge ${normalized}`}>{normalized}</span>;
}

export function Empty({
  children,
}: {
  children: ReactNode;
}) {
  return <div className="empty">{children}</div>;
}

export function SectionTitle({
  title,
  subtitle,
  action,
}: {
  title: string;
  subtitle?: string;
  action?: ReactNode;
}) {
  return (
    <div className="section-title">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

export function StatusLine({
  label,
  value,
  status = "ok",
}: {
  label: string;
  value: string;
  status?: "ok" | "warn" | "error";
}) {
  return (
    <div className="status-line">
      <span className={`status-dot ${status}`} />
      <span>{label}</span>
      <b>{value}</b>
    </div>
  );
}

export function MiniTrend({
  values,
}: {
  values: number[];
}) {
  if (!values.length) return null;
  const max = Math.max(...values);
  const min = Math.min(...values);
  const points = values
    .map((v, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * 100;
      const y =
        36 -
        ((v - min) / Math.max(max - min, 1)) * 30;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <svg
      className="mini-trend"
      viewBox="0 0 100 40"
      preserveAspectRatio="none"
      aria-hidden
    >
      <polyline points={points} fill="none" />
    </svg>
  );
}

export function RiskGauge({
  probability,
}: {
  probability: number;
}) {
  const pct = Math.max(0, Math.min(100, probability * 100));
  const level =
    pct >= 70 ? "high" : pct >= 40 ? "medium" : "low";

  return (
    <div className={`risk-gauge ${level}`}>
      <div
        className="risk-gauge-ring"
        style={{
          background: `conic-gradient(var(--gauge) ${pct * 3.6}deg, rgba(255,255,255,.06) 0deg)`,
        }}
      >
        <div className="risk-gauge-inner">
          <strong>{pct.toFixed(0)}%</strong>
          <span>delay risk</span>
        </div>
      </div>
      <RiskBadge level={level} />
    </div>
  );
}

export function ToolActivity({
  steps,
  elapsed,
  active,
}: {
  steps: {
    label: string;
    detail: string;
    state: "waiting" | "active" | "done";
  }[];
  elapsed: number;
  active: boolean;
}) {
  return (
    <Card className="tool-activity">
      <div className="activity-head">
        <div>
          <span className="activity-kicker">
            <Sparkles size={13} />
            SupplyMind reasoning trace
          </span>
          <h3>
            {active ? "Investigating your request" : "Investigation complete"}
          </h3>
        </div>
        <span className="elapsed">
          <Clock3 size={13} /> {elapsed.toFixed(1)}s
        </span>
      </div>

      <div className="activity-steps">
        {steps.map((step) => (
          <div
            key={step.label}
            className={`activity-step ${step.state}`}
          >
            <div className="activity-node">
              {step.state === "done" ? (
                <CheckCircle2 size={16} />
              ) : step.state === "active" ? (
                <Activity size={16} />
              ) : (
                <ChevronRight size={16} />
              )}
            </div>
            <div>
              <b>{step.label}</b>
              <small>{step.detail}</small>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export function InsightRow({
  title,
  description,
  tone = "default",
}: {
  title: string;
  description: string;
  tone?: "default" | "danger" | "warning" | "success";
}) {
  return (
    <div className={`insight-row ${tone}`}>
      <div className="insight-icon">
        {tone === "danger" ? (
          <AlertTriangle size={15} />
        ) : (
          <ArrowUpRight size={15} />
        )}
      </div>
      <div>
        <b>{title}</b>
        <p>{description}</p>
      </div>
    </div>
  );
}
