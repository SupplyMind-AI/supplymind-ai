import { useEffect, useMemo, useRef, useState } from "react";
import {
  Globe2,
  RefreshCcw,
  SlidersHorizontal,
  TriangleAlert,
} from "lucide-react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

import { api, safeApi } from "../api";
import {
  AsyncButton,
  Card,
  Header,
  RiskBadge,
  SectionTitle,
} from "../components";

function severityLevel(value: number) {
  return value >= 0.7 ? "high" : value >= 0.4 ? "medium" : "low";
}

function markerIcon(level: "high" | "medium" | "low") {
  return L.divIcon({
    className: "supplymind-marker-shell",
    html: `<span class="supplymind-marker ${level}"><i></i></span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

function LeafletEventMap({
  events,
  selectedId,
  onSelect,
}: {
  events: any[];
  selectedId?: string | number;
  onSelect: (event: any) => void;
}) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<L.Map | null>(null);
  const layerRef = useRef<L.LayerGroup | null>(null);

  useEffect(() => {
    if (!containerRef.current || mapRef.current) return;

    const map = L.map(containerRef.current, {
      zoomControl: false,
      attributionControl: true,
      worldCopyJump: true,
    }).setView([28, 5], 2);

    L.control.zoom({ position: "topright" }).addTo(map);

    L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
      {
        attribution:
          '&copy; OpenStreetMap contributors &copy; CARTO',
        maxZoom: 19,
      },
    ).addTo(map);

    layerRef.current = L.layerGroup().addTo(map);
    mapRef.current = map;

    window.setTimeout(() => map.invalidateSize(), 50);

    return () => {
      map.remove();
      mapRef.current = null;
      layerRef.current = null;
    };
  }, []);

  useEffect(() => {
    if (!mapRef.current || !layerRef.current) return;

    layerRef.current.clearLayers();

    const bounds: L.LatLngTuple[] = [];

    events.forEach((event) => {
      const latitude = Number(event.latitude);
      const longitude = Number(event.longitude);
      if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
        return;
      }

      const level = severityLevel(Number(event.severity ?? 0));
      const marker = L.marker([latitude, longitude], {
        icon: markerIcon(level),
        zIndexOffset: String(event.id) === String(selectedId) ? 1000 : 0,
      });

      marker.bindTooltip(
        `
          <div class="map-tooltip">
            <b>${event.title ?? "Supply-chain event"}</b>
            <span>${[event.region, event.country].filter(Boolean).join(", ") || "Global"}</span>
            <small>Severity ${Number(event.severity ?? 0).toFixed(2)}</small>
          </div>
        `,
        {
          direction: "top",
          offset: [0, -12],
          opacity: 1,
          className: "supplymind-map-tooltip",
        },
      );

      marker.on("click", () => onSelect(event));
      marker.addTo(layerRef.current!);
      bounds.push([latitude, longitude]);
    });

    if (bounds.length > 1) {
      mapRef.current.fitBounds(bounds, {
        padding: [45, 45],
        maxZoom: 4,
      });
    } else if (bounds.length === 1) {
      mapRef.current.setView(bounds[0], 4);
    }
  }, [events, selectedId, onSelect]);

  return <div className="leaflet-event-map" ref={containerRef} />;
}

export default function Events() {
  const [data, setData] = useState<any[]>([]);
  const [type, setType] = useState("");
  const [severity, setSeverity] = useState("");
  const [selected, setSelected] = useState<any>(null);
  const [refreshing, setRefreshing] = useState(false);
  const [refreshNotice, setRefreshNotice] = useState("");

  async function load() {
    setData(await safeApi<any[]>("/events", []));
  }

  useEffect(() => {
    void load();
  }, []);

  async function refresh() {
    setRefreshing(true);
    setRefreshNotice("");

    try {
      await api("/events/refresh", { method: "POST" });
      await load();
    } catch {
      setRefreshNotice(
        "External intelligence refresh is temporarily rate-limited. Displaying the latest stored event data.",
      );
    } finally {
      setRefreshing(false);
    }
  }

  const types = [...new Set(data.map((x) => x.event_type).filter(Boolean))];

  const shown = useMemo(() => {
    return data.filter((event) => {
      const typeMatch = !type || event.event_type === type;
      const level = severityLevel(Number(event.severity ?? 0));
      return typeMatch && (!severity || level === severity);
    });
  }, [data, type, severity]);

  const geocoded = shown.filter(
    (event) =>
      Number.isFinite(Number(event.latitude)) &&
      Number.isFinite(Number(event.longitude)),
  );

  return (
    <>
      <Header
        eyebrow="GDELT · EXTERNAL INTELLIGENCE"
        title="Event Monitor"
        subtitle="Global logistics disruptions normalized into operational risk signals."
        action={
          <AsyncButton
            loading={refreshing}
            loadingText="Refreshing"
            className="primary"
            onClick={refresh}
          >
            <RefreshCcw size={16} />
            Refresh intelligence
          </AsyncButton>
        }
      />

      {refreshNotice && (
        <div className="graceful-notice">
          <TriangleAlert size={16} />
          <span>{refreshNotice}</span>
        </div>
      )}

      <Card className="map-card">
        <SectionTitle
          title="Global disruption map"
          subtitle={`${geocoded.length} geocoded events · ${shown.length} active signals`}
          action={<Globe2 size={19} />}
        />

        <div className="map-filter-row">
          <div>
            <SlidersHorizontal size={15} />
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

        <div className="leaflet-map-shell">
          <LeafletEventMap
            events={geocoded}
            selectedId={selected?.id}
            onSelect={setSelected}
          />

          <div className="map-legend-v2">
            <span><i className="high" /> High</span>
            <span><i className="medium" /> Medium</span>
            <span><i className="low" /> Low</span>
          </div>

          {!geocoded.length && (
            <div className="map-empty-overlay">
              <Globe2 size={34} />
              <b>No geocoded event signals yet</b>
              <p>
                Refresh intelligence when the external provider is
                available. Stored events will remain visible between
                refreshes.
              </p>
            </div>
          )}
        </div>

        {selected && (
          <div className="selected-event-panel">
            <div>
              <span>SELECTED EVENT</span>
              <h3>{selected.title}</h3>
              <p>
                {[selected.region, selected.country]
                  .filter(Boolean)
                  .join(", ") || "Global"}
              </p>
            </div>
            <RiskBadge
              level={severityLevel(Number(selected.severity ?? 0))}
            />
          </div>
        )}
      </Card>

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
                  {event.description?.slice(0, 135)}
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
                  level={severityLevel(Number(event.severity ?? 0))}
                />{" "}
                {Number(event.severity ?? 0).toFixed(2)}
              </span>
            </div>
          ))}

          {!shown.length && (
            <div className="premium-empty-state compact">
              <Globe2 size={27} />
              <b>No event data available</b>
              <p>
                The application remains operational. Retry external
                intelligence later.
              </p>
            </div>
          )}
        </div>
      </Card>
    </>
  );
}
