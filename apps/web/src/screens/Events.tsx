import { useCallback, useEffect, useMemo, useState } from "react";

import { api } from "../api";
import { Card, Header, RiskBadge } from "../components";

type SupplyChainEvent = {
  id: string;
  title: string;
  description?: string | null;
  event_type: string;
  severity?: number | null;
  country?: string | null;
  region?: string | null;
  latitude?: number | null;
  longitude?: number | null;
};

type EventMapProps = {
  events: SupplyChainEvent[];
};

function project(latitude: number, longitude: number) {
  return {
    x: ((longitude + 180) / 360) * 100,
    y: ((90 - latitude) / 180) * 100,
  };
}

function EventMap({ events }: EventMapProps) {
  const plottableEvents = events.filter(
    (event) =>
      typeof event.latitude === "number" &&
      typeof event.longitude === "number",
  );

  return (
    <div
      className="event-map"
      style={{
        position: "relative",
        minHeight: 360,
        overflow: "hidden",
        borderRadius: 18,
        background:
          "radial-gradient(circle at 50% 30%, rgba(74, 95, 255, 0.18), transparent 38%), linear-gradient(180deg, #111a35 0%, #0b1226 100%)",
        border: "1px solid rgba(255,255,255,0.08)",
      }}
    >
      {plottableEvents.map((event) => {
        const point = project(event.latitude!, event.longitude!);
        const severity = event.severity ?? 0;

        return (
          <button
            key={event.id}
            type="button"
            title={`${event.title} · severity ${severity.toFixed(2)}`}
            aria-label={event.title}
            style={{
              position: "absolute",
              left: `${point.x}%`,
              top: `${point.y}%`,
              width: severity >= 0.7 ? 16 : 12,
              height: severity >= 0.7 ? 16 : 12,
              transform: "translate(-50%, -50%)",
              borderRadius: "50%",
              border: "2px solid rgba(255,255,255,.9)",
              background:
                severity >= 0.7
                  ? "#ff5a79"
                  : severity >= 0.4
                    ? "#ffb347"
                    : "#6ee7b7",
              boxShadow: "0 0 0 5px rgba(99,102,241,.18)",
              cursor: "pointer",
            }}
          />
        );
      })}

      <div
        style={{
          position: "absolute",
          left: 16,
          bottom: 14,
          padding: "7px 10px",
          borderRadius: 10,
          background: "rgba(5,10,25,.72)",
          color: "rgba(255,255,255,.72)",
          fontSize: 12,
        }}
      >
        {plottableEvents.length} geocoded events
      </div>
    </div>
  );
}

export default function Events() {
  const [events, setEvents] = useState<SupplyChainEvent[]>([]);
  const [type, setType] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setError(null);
    try {
      const data = await api<SupplyChainEvent[]>("/events");
      setEvents(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to load events.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function refresh() {
    setRefreshing(true);
    setError(null);
    try {
      await api<unknown>("/events/refresh", { method: "POST" });
      await load();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to refresh external intelligence.",
      );
    } finally {
      setRefreshing(false);
    }
  }

  const types = useMemo(
    () =>
      Array.from(
        new Set(
          events
            .map((event) => event.event_type)
            .filter((eventType): eventType is string => Boolean(eventType)),
        ),
      ).sort(),
    [events],
  );

  const shown = useMemo(
    () =>
      type ? events.filter((event) => event.event_type === type) : events,
    [events, type],
  );

  return (
    <>
      <Header
        title="Event Monitor"
        subtitle="Global supply-chain disruptions normalized from external intelligence."
        action={
          <button
            className="primary"
            type="button"
            onClick={() => void refresh()}
            disabled={refreshing}
          >
            {refreshing ? "Refreshing…" : "Refresh intelligence"}
          </button>
        }
      />

      {error && (
        <Card>
          <p role="alert">{error}</p>
        </Card>
      )}

      <Card>
        <div className="event-toolbar">
          <select
            value={type}
            onChange={(event) => setType(event.target.value)}
            aria-label="Filter by event type"
          >
            <option value="">All event types</option>
            {types.map((eventType) => (
              <option key={eventType} value={eventType}>
                {eventType}
              </option>
            ))}
          </select>
          <span>{loading ? "Loading events…" : `${shown.length} active events`}</span>
        </div>

        <EventMap events={shown} />
      </Card>

      <Card>
        <div className="table header-row event-head">
          <div>Event</div>
          <div>Location</div>
          <div>Type</div>
          <div>Severity</div>
        </div>

        {!loading && shown.length === 0 && (
          <div className="empty-state">No active events match this filter.</div>
        )}

        {shown.map((event) => {
          const severity = event.severity ?? 0;
          const riskLevel =
            severity >= 0.7 ? "high" : severity >= 0.4 ? "medium" : "low";

          return (
            <div className="event-row" key={event.id}>
              <div>
                <b>{event.title}</b>
                <small>{event.description?.slice(0, 120) || "—"}</small>
              </div>
              <div>
                {[event.region, event.country].filter(Boolean).join(", ") || "—"}
              </div>
              <div>
                <span className="type-pill">{event.event_type}</span>
              </div>
              <div>
                <RiskBadge level={riskLevel} />{" "}
                {typeof event.severity === "number"
                  ? event.severity.toFixed(2)
                  : "—"}
              </div>
            </div>
          );
        })}
      </Card>
    </>
  );
}
