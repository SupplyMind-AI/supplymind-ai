import { useEffect, useMemo, useState } from "react";
import {
  Globe2,
  RefreshCcw,
  SlidersHorizontal,
} from "lucide-react";
import { api, safeApi } from "../api";
import {
  Card,
  Header,
  RiskBadge,
  SectionTitle,
} from "../components";

function project(latitude: number, longitude: number) {
  return {
    x: ((longitude + 180) / 360) * 100,
    y: ((90 - latitude) / 180) * 100,
  };
}

export default function Events() {
  const [data, setData] = useState<any[]>([]);
  const [type, setType] = useState("");
  const [severity, setSeverity] = useState("");
  const [selected, setSelected] = useState<any>(null);
  const [refreshing, setRefreshing] = useState(false);

  async function load() {
    setData(await safeApi<any[]>("/events", []));
  }

  useEffect(() => {
    void load();
  }, []);

  async function refresh() {
    setRefreshing(true);
    try {
      await api("/events/refresh", { method: "POST" });
      await load();
    } finally {
      setRefreshing(false);
    }
  }

  const types = [...new Set(data.map((x) => x.event_type).filter(Boolean))];

  const shown = useMemo(() => {
    return data.filter((event) => {
      const typeMatch = !type || event.event_type === type;
      const eventSeverity = Number(event.severity ?? 0);
      const level =
        eventSeverity >= 0.7
          ? "high"
          : eventSeverity >= 0.4
            ? "medium"
            : "low";

      return typeMatch && (!severity || level === severity);
    });
  }, [data, type, severity]);

  const geocoded = shown.filter(
    (event) =>
      typeof event.latitude === "number" &&
      typeof event.longitude === "number",
  );

  return (
    <>
      <Header
        eyebrow="GDELT · EXTERNAL INTELLIGENCE"
        title="Event Monitor"
        subtitle="Global logistics disruptions normalized into operational risk signals."
        action={
          <button
            className="primary"
            onClick={refresh}
            disabled={refreshing}
          >
            <RefreshCcw size={15} />
            {refreshing ? "Refreshing…" : "Refresh intelligence"}
          </button>
        }
      />

      <div className="event-layout">
        <Card className="map-card">
          <SectionTitle
            title="Global disruption map"
            subtitle={`${geocoded.length} geocoded events · ${shown.length} active signals`}
            action={<Globe2 size={18} />}
          />

          <div className="map-filter-row">
            <div>
              <SlidersHorizontal size={14} />
              <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="">All event types</option>
                {types.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </div>
            <select
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
            >
              <option value="">All severities</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
          </div>

          <div className="world-map">
            <div className="world-grid" />
            <div className="continent continent-na" />
            <div className="continent continent-sa" />
            <div className="continent continent-eu" />
            <div className="continent continent-af" />
            <div className="continent continent-as" />
            <div className="continent continent-au" />

            {geocoded.map((event, index) => {
              const point = project(
                event.latitude,
                event.longitude,
              );
              const level =
                Number(event.severity ?? 0) >= 0.7
                  ? "high"
                  : Number(event.severity ?? 0) >= 0.4
                    ? "medium"
                    : "low";

              return (
                <button
                  key={event.id ?? index}
                  className={`map-pin ${level} ${
                    selected?.id === event.id ? "selected" : ""
                  }`}
                  style={{
                    left: `${point.x}%`,
                    top: `${point.y}%`,
                  }}
                  onClick={() => setSelected(event)}
                  title={event.title}
                >
                  <span />
                </button>
              );
            })}

            <div className="map-legend">
              <span><i className="high" /> High</span>
              <span><i className="medium" /> Medium</span>
              <span><i className="low" /> Low</span>
            </div>
          </div>

          {selected && (
            <div className="map-detail-popover">
              <div>
                <b>{selected.title}</b>
                <p>
                  {[selected.region, selected.country]
                    .filter(Boolean)
                    .join(", ") || "Global"}
                </p>
              </div>
              <RiskBadge
                level={
                  Number(selected.severity ?? 0) >= 0.7
                    ? "high"
                    : Number(selected.severity ?? 0) >= 0.4
                      ? "medium"
                      : "low"
                }
              />
            </div>
          )}
        </Card>
      </div>

      <Card>
        <SectionTitle
          title="Active intelligence feed"
          subtitle="Normalized events with severity and location context"
        />

        <div className="premium-table">
          <div className="premium-table-head four">
            <span>Event</span>
            <span>Location</span>
            <span>Type</span>
            <span>Severity</span>
          </div>

          {shown.map((event, index) => (
            <div
              className="premium-table-row four interactive"
              key={event.id ?? index}
              onClick={() => setSelected(event)}
            >
              <div>
                <b>{event.title}</b>
                <small>
                  {event.description?.slice(0, 120)}
                </small>
              </div>
              <span>
                {[event.region, event.country]
                  .filter(Boolean)
                  .join(", ") || "—"}
              </span>
              <span className="type-pill">{event.event_type}</span>
              <span>
                <RiskBadge
                  level={
                    Number(event.severity ?? 0) >= 0.7
                      ? "high"
                      : Number(event.severity ?? 0) >= 0.4
                        ? "medium"
                        : "low"
                  }
                />{" "}
                {Number(event.severity ?? 0).toFixed(2)}
              </span>
            </div>
          ))}
        </div>
      </Card>
    </>
  );
}
