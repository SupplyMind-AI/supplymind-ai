import type { ReactNode } from "react";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  ArrowUpRight,
  CheckCircle2,
  ChevronRight,
  LoaderCircle,
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
      initial={{ opacity: 0, y: 10, scale: 0.995 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
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

export function LoadingDots({ label = "Loading" }: { label?: string }) {
  return (
    <span className="loading-dots" aria-label={label}>
      <span />
      <span />
      <span />
    </span>
  );
}

export function AsyncButton({
  loading,
  children,
  className = "primary",
  loadingText = "Working",
  ...props
}: {
  loading: boolean;
  children: ReactNode;
  className?: string;
  loadingText?: string;
} & React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      className={`${className} ${loading ? "button-busy" : ""}`}
      disabled={loading || props.disabled}
    >
      {loading ? (
        <>
          <span className="orbit-loader">
            <i />
            <i />
            <i />
          </span>
          <span>{loadingText}</span>
        </>
      ) : (
        children
      )}
    </button>
  );
}

export function ScreenProgress({ visible }: { visible: boolean }) {
  return (
    <div className={`screen-progress ${visible ? "visible" : ""}`}>
      <span />
    </div>
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
    <motion.div
      className={`risk-gauge ${level}`}
      initial={{ opacity: 0, scale: 0.88 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ type: "spring", stiffness: 180, damping: 16 }}
      whileHover={{ scale: 1.04 }}
    >
      <div
        className="risk-gauge-ring"
        style={{
          background: `conic-gradient(var(--gauge) ${pct * 3.6}deg, rgba(255,255,255,.07) 0deg)`,
        }}
      >
        <div className="risk-gauge-inner">
          <strong>{pct.toFixed(0)}%</strong>
          <span>delay risk</span>
        </div>
      </div>
      <RiskBadge level={level} />
    </motion.div>
  );
}

export function MiniTrend({
  values,
  labels,
}: {
  values: number[];
  labels?: string[];
}) {
  if (!values.length) return null;

  const max = Math.max(...values);
  const min = Math.min(...values);
  const points = values
    .map((v, index) => {
      const x = (index / Math.max(values.length - 1, 1)) * 100;
      const y =
        90 -
        ((v - min) / Math.max(max - min, 1)) * 70;
      return `${x},${y}`;
    })
    .join(" ");

  return (
    <div className="hover-chart">
      <svg
        className="mini-trend"
        viewBox="0 0 100 100"
        preserveAspectRatio="none"
        aria-hidden
      >
        <defs>
          <linearGradient id="areaGradient" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#8b63ff" stopOpacity=".45" />
            <stop offset="100%" stopColor="#8b63ff" stopOpacity="0" />
          </linearGradient>
        </defs>
        <polygon
          points={`0,100 ${points} 100,100`}
          fill="url(#areaGradient)"
        />
        <polyline points={points} fill="none" />
      </svg>

      <div className="chart-hover-points">
        {values.map((value, index) => {
          const x = (index / Math.max(values.length - 1, 1)) * 100;
          const y =
            90 -
            ((value - min) / Math.max(max - min, 1)) * 70;
          return (
            <motion.div
              key={`${value}-${index}`}
              className="chart-point"
              style={{ left: `${x}%`, top: `${y}%` }}
              whileHover={{ scale: 1.55 }}
            >
              <span className="chart-tooltip">
                <b>{value.toFixed(1)}%</b>
                <small>{labels?.[index] ?? `Point ${index + 1}`}</small>
              </span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}

export function DonutChart({
  segments,
  centerLabel,
  centerValue,
}: {
  segments: Array<{
    label: string;
    value: number;
    tone: "high" | "medium" | "low";
  }>;
  centerLabel: string;
  centerValue: string | number;
}) {
  const total = Math.max(
    1,
    segments.reduce((sum, segment) => sum + segment.value, 0),
  );
  const colors = {
    high: "#ff5f7d",
    medium: "#ffb94a",
    low: "#3ddb94",
  };

  let cursor = 0;
  const stops: string[] = [];
  for (const segment of segments) {
    const start = cursor;
    cursor += (segment.value / total) * 100;
    stops.push(
      `${colors[segment.tone]} ${start}% ${Math.max(start, cursor)}%`,
    );
  }

  return (
    <div className="donut-wrap">
      <motion.div
        className="risk-donut interactive-donut"
        style={{
          background: `conic-gradient(${stops.join(",")})`,
        }}
        initial={{ rotate: -80, scale: 0.82, opacity: 0 }}
        animate={{ rotate: 0, scale: 1, opacity: 1 }}
        transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] }}
        whileHover={{ scale: 1.045 }}
      >
        <div>
          <strong>{centerValue}</strong>
          <span>{centerLabel}</span>
        </div>
      </motion.div>

      <div className="donut-legend">
        {segments.map((segment) => (
          <motion.div
            key={segment.label}
            className="donut-legend-row"
            whileHover={{ x: 4 }}
          >
            <i className={segment.tone} />
            <span>{segment.label}</span>
            <b>{segment.value}</b>
            <small>
              {((segment.value / total) * 100).toFixed(0)}%
            </small>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export function BarChart({
  rows,
}: {
  rows: Array<{
    label: string;
    value: number;
    note?: string;
  }>;
}) {
  const max = Math.max(1, ...rows.map((row) => row.value));

  return (
    <div className="bar-chart">
      {rows.map((row) => (
        <motion.div
          key={row.label}
          className="bar-row"
          whileHover={{ x: 3 }}
        >
          <div className="bar-label">
            <span>{row.label}</span>
            <b>{row.value.toFixed(1)}%</b>
          </div>
          <div className="bar-track">
            <motion.div
              className="bar-fill"
              initial={{ width: 0 }}
              animate={{ width: `${(row.value / max) * 100}%` }}
              transition={{ duration: 0.65, ease: [0.16, 1, 0.3, 1] }}
            >
              <span className="bar-tooltip">
                {row.note ?? `${row.value.toFixed(1)}%`}
              </span>
            </motion.div>
          </div>
        </motion.div>
      ))}
    </div>
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
    <motion.div
      className={`insight-row ${tone}`}
      whileHover={{ x: 4 }}
    >
      <div className="insight-icon">
        {tone === "danger" ? (
          <AlertTriangle size={16} />
        ) : (
          <ArrowUpRight size={16} />
        )}
      </div>
      <div>
        <b>{title}</b>
        <p>{description}</p>
      </div>
    </motion.div>
  );
}

export function ClaudeTrace({
  visible,
  steps,
  elapsed,
}: {
  visible: boolean;
  steps: Array<{
    label: string;
    detail: string;
    state: "waiting" | "active" | "done";
  }>;
  elapsed: number;
}) {
  if (!visible && !steps.some((step) => step.state === "done")) {
    return null;
  }

  return (
    <motion.div
      className="claude-trace"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="claude-trace-head">
        <div className="claude-orb">
          <Sparkles size={14} />
          <span />
        </div>
        <div>
          <b>{visible ? "Working through your request" : "Reasoning complete"}</b>
          <small>{elapsed.toFixed(1)}s</small>
        </div>
      </div>

      <div className="claude-trace-body">
        {steps.map((step) => (
          <motion.div
            className={`claude-trace-step ${step.state}`}
            key={step.label}
            animate={
              step.state === "active"
                ? { opacity: [0.45, 1, 0.45] }
                : { opacity: 1 }
            }
            transition={
              step.state === "active"
                ? { duration: 1.2, repeat: Infinity }
                : undefined
            }
          >
            <span className="trace-symbol">
              {step.state === "done" ? (
                <CheckCircle2 size={14} />
              ) : step.state === "active" ? (
                <LoaderCircle size={14} />
              ) : (
                <ChevronRight size={14} />
              )}
            </span>
            <div>
              <b>{step.label}</b>
              <small>{step.detail}</small>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

export function HighRiskRecommendations({
  probability,
  drivers = [],
}: {
  probability: number;
  drivers?: string[];
}) {
  if (probability < 0.7) return null;

  const steps = [
    {
      title: "Validate the disruption context",
      detail:
        "Check weather and external-event evidence for the route before escalating.",
    },
    {
      title: "Protect the delivery promise",
      detail:
        "Review alternate carrier/service options and add operational buffer where possible.",
    },
    {
      title: "Notify the responsible owner",
      detail:
        "Create a risk alert and assign the shipment for active monitoring.",
    },
    {
      title: "Prepare customer communication",
      detail:
        "If the risk remains high, proactively communicate the potential delay and next update window.",
    },
  ];

  return (
    <div className="recommendation-panel">
      <div className="recommendation-head">
        <div className="recommendation-icon">
          <Sparkles size={17} />
        </div>
        <div>
          <span>HIGH-RISK PLAYBOOK</span>
          <h3>Recommended next actions</h3>
          <p>
            Prioritized actions based on the current prediction
            {drivers.length ? ` and ${drivers.length} identified drivers` : ""}.
          </p>
        </div>
      </div>

      <div className="recommendation-steps">
        {steps.map((step, index) => (
          <motion.div
            key={step.title}
            className="recommendation-step"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.08 }}
          >
            <span>{index + 1}</span>
            <div>
              <b>{step.title}</b>
              <small>{step.detail}</small>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
