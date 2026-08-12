import { useEffect, useMemo, useState } from "react";
import {
  CircleMarker,
  MapContainer,
  Popup,
  TileLayer,
} from "react-leaflet";

import { api } from "../api";
import { Card, Header, RiskBadge } from "../components";

type Event = {
  id: string;
  title: string;
  description?: string | null;
  event_type: string;
  severity?: number | null;
  country?: string | null;
  region?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  source?: string | null;
  source_url?: string | null;
};

function severityLevel(severity = 0) {
  if (severity >= 0.7) return "high";
  if (severity >= 0.4) return "medium";
  return "low";
}

function markerColor(severity = 0) {
  if (severity >= 0.7) return "#ff496f";
  if (severity >= 0.4) return "#ffb33f";
  return "#37d689";
}

function EventMap({ events }: { events: Event[] }) {
  const geocoded = events.filter(
    (event) =>
      typeof event.latitude === "number" &&
      typeof event.longitude === "number"
  );

  return (
    <div className="event-map">
      <MapContainer
        center={[25, 10]}
        zoom={2}
        minZoom={2}
        scrollWheelZoom
        className="leaflet-event-map"
      >
        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {geocoded.map((event) => {
          const severity = event.severity ?? 0;

          return (
            <CircleMarker
              key={event.id}
              center={[event.latitude!, event.longitude!]}
              radius={severity >= 0.7 ? 9 : 7}
              pathOptions={{
                color: markerColor(severity),
                fillColor: markerColor(severity),
                fillOpacity: 0.9,
                weight: 2,
              }}
            >
              <Popup>
                <div className="event-popup">
                  <strong>{event.title}</strong>

                  <p>
                    {[event.region, event.country]
                      .filter(Boolean)
                      .join(", ") || "Unknown location"}
                  </p>

                  <div>
                    <b>Type:</b>{" "}
                    {event.event_type.replaceAll("_", " ")}
                  </div>

                  <div>
                    <b>Severity:</b>{" "}
                    {(event.severity ?? 0).toFixed(2)}
                  </div>

                  {event.description && (
                    <p>{event.description.slice(0, 220)}</p>
                  )}

                  {event.source && (
                    <small>Source: {event.source.toUpperCase()}</small>
                  )}
                </div>
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>

      <div className="map-count">
        {geocoded.length} geocoded events
      </div>
    </div>
  );
}

export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [type, setType] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    try {
      setError("");
      const data = await api<Event[]>("/events");
      setEvents(data);
    } catch (err) {
      setError(String(err));
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function refresh() {
    setRefreshing(true);

    try {
      setError("");

      await api("/events/refresh", {
        method: "POST",
      });

      await load();
    } catch (err) {
      setError(String(err));
    } finally {
      setRefreshing(false);
    }
  }

  const types = useMemo(
    () => [...new Set(events.map((event) => event.event_type))].sort(),
    [events]
  );

  const shown = useMemo(
    () =>
      type
        ? events.filter((event) => event.event_type === type)
        : events,
    [events, type]
  );

  return (
    <>
      <Header
        title="Event Monitor"
        subtitle="Global supply-chain disruptions normalized from external intelligence."
        action={
          <button
            className="primary"
            onClick={refresh}
            disabled={refreshing}
          >
            {refreshing
              ? "Refreshing intelligence…"
              : "Refresh intelligence"}
          </button>
        }
      />

      {error && <p className="error">{error}</p>}

      <Card>
        <div className="event-toolbar">
          <select
            value={type}
            onChange={(event) => setType(event.target.value)}
          >
            <option value="">All event types</option>

            {types.map((eventType) => (
              <option key={eventType} value={eventType}>
                {eventType.replaceAll("_", " ")}
              </option>
            ))}
          </select>

          <span>{shown.length} active events</span>
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

        {shown.map((event) => {
          const level = severityLevel(event.severity ?? 0);

          return (
            <div className="event-row" key={event.id}>
              <div>
                <b>{event.title}</b>

                {event.description && (
                  <small>
                    {event.description.slice(0, 120)}
                  </small>
                )}
              </div>

              <div>
                {[event.region, event.country]
                  .filter(Boolean)
                  .join(", ") || "—"}
              </div>

              <div>
                <span className="type-pill">
                  {event.event_type.replaceAll("_", " ")}
                </span>
              </div>

              <div>
                <RiskBadge level={level} />{" "}
                {event.severity?.toFixed(2) ?? "—"}
              </div>
            </div>
          );
        })}
      </Card>
    </>
  );
}