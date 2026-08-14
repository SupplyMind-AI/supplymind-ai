import {
  ChangeEvent,
  FormEvent,
  useMemo,
  useRef,
  useState,
} from "react";
import {
  CheckCircle2,
  CloudUpload,
  FileSpreadsheet,
  Filter,
  PackagePlus,
  Sparkles,
  WandSparkles,
} from "lucide-react";
import { api } from "../api";
import {
  AsyncButton,
  Card,
  Header,
  HighRiskRecommendations,
  InsightRow,
  RiskGauge,
  RiskBadge,
  SectionTitle,
} from "../components";
import { predictionView } from "../predictionView";

const initial = {
  external_id: "TEST-BERLIN-001",
  payment_type: "DEBIT",
  category_name: "Sporting Goods",
  customer_country: "Germany",
  customer_segment: "Consumer",
  customer_state: "Berlin",
  department_name: "Sports",
  market: "Europe",
  order_country: "Germany",
  order_region: "Western Europe",
  product_name: "Training Equipment",
  shipping_mode: "Standard Class",
  customer_city: "Berlin",
  order_city: "Hamburg",
  order_state: "Hamburg",
  profit_per_order: 20,
  sales_per_customer: 120,
  latitude: 52.52,
  longitude: 13.405,
  order_item_discount: 0,
  order_item_discount_rate: 0,
  order_item_product_price: 120,
  order_item_profit_ratio: 0.15,
  order_item_quantity: 1,
  sales: 120,
  order_item_total_amount: 120,
  order_profit_per_order: 20,
  product_price: 120,
};

function buildPredictionPayload(input: any) {
  const { external_id, ...features } = input;
  const order_date = new Date().toISOString();

  return {
    external_id,
    order_date,
    features: {
      ...features,
      order_date,
    },
  };
}

function parseCsv(text: string) {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  if (lines.length < 2) return [];

  const headers = lines[0]
    .split(",")
    .map((header) => header.trim());

  return lines.slice(1).map((line) => {
    const cells = line.split(",").map((cell) => cell.trim());
    const record: Record<string, any> = {};
    headers.forEach((header, index) => {
      record[header] = cells[index] ?? "";
    });
    return record;
  });
}

function coerceCsvRow(row: Record<string, any>, index: number) {
  const numericKeys = new Set([
    "profit_per_order",
    "sales_per_customer",
    "latitude",
    "longitude",
    "order_item_discount",
    "order_item_discount_rate",
    "order_item_product_price",
    "order_item_profit_ratio",
    "order_item_quantity",
    "sales",
    "order_item_total_amount",
    "order_profit_per_order",
    "product_price",
  ]);

  const merged: any = {
    ...initial,
    ...row,
    external_id:
      row.external_id ||
      row.shipment_id ||
      `CSV-SHIPMENT-${String(index + 1).padStart(3, "0")}`,
  };

  for (const key of numericKeys) {
    if (merged[key] !== "" && merged[key] != null) {
      merged[key] = Number(merged[key]);
    }
  }

  return merged;
}

export default function Prediction({
  onAsk,
}: {
  onAsk: () => void;
}) {
  const [mode, setMode] = useState<"single" | "csv">("single");
  const [form, setForm] = useState<any>(initial);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [csvRows, setCsvRows] = useState<any[]>([]);
  const [csvResults, setCsvResults] = useState<any[]>([]);
  const [batchProgress, setBatchProgress] = useState(0);
  const [batchRisk, setBatchRisk] = useState("all");
  const [batchDecision, setBatchDecision] = useState("all");
  const [batchProbability, setBatchProbability] = useState("all");
  const fileRef = useRef<HTMLInputElement | null>(null);

  const set = (key: string, value: any) =>
    setForm((previous: any) => ({
      ...previous,
      [key]: value,
    }));

  async function go(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await api<any>("/predictions", {
        method: "POST",
        body: JSON.stringify(buildPredictionPayload(form)),
      });
      setResult(response);
    } catch (caught) {
      setError(String(caught));
    } finally {
      setLoading(false);
    }
  }

  async function handleCsv(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) return;

    const text = await file.text();
    const parsed = parseCsv(text).map(coerceCsvRow);
    setCsvRows(parsed);
    setCsvResults([]);
    setBatchProgress(0);
  }

  async function runBatch() {
    setLoading(true);
    setError("");
    setCsvResults([]);
    setBatchProgress(0);

    const results: any[] = [];

    try {
      for (let index = 0; index < csvRows.length; index += 1) {
        const row = csvRows[index];
        try {
          const response = await api<any>("/predictions", {
            method: "POST",
            body: JSON.stringify(buildPredictionPayload(row)),
          });
          results.push({
            external_id: row.external_id,
            ok: true,
            ...response,
          });
        } catch (caught) {
          results.push({
            external_id: row.external_id,
            ok: false,
            error: String(caught),
          });
        }

        setBatchProgress(
          Math.round(((index + 1) / csvRows.length) * 100),
        );
      }

      setCsvResults(results);
    } finally {
      setLoading(false);
    }
  }

  const currentPrediction =
    result ? predictionView(result) : null;

  const probability =
    currentPrediction?.probability ?? 0;

  const explanation =
    result?.explanation ??
    result?.reason ??
    result?.summary ??
    "Prediction is generated by the active champion pipeline using the shipment features provided.";

  const normalizedCsvResults = useMemo(
    () =>
      csvResults.map((item, index) => ({
        item,
        index,
        view: item.ok ? predictionView(item) : null,
      })),
    [csvResults],
  );

  const shownCsvResults = useMemo(
    () =>
      normalizedCsvResults.filter(({ item, view }) => {
        if (!item.ok || !view) {
          return (
            batchRisk === "all" &&
            batchDecision === "all" &&
            batchProbability === "all"
          );
        }

        const riskMatch =
          batchRisk === "all" || view.riskLevel === batchRisk;

        const decisionMatch =
          batchDecision === "all" ||
          (batchDecision === "delay" && view.isDelayed) ||
          (batchDecision === "track" && !view.isDelayed);

        const probabilityMatch =
          batchProbability === "all" ||
          (batchProbability === "lt40" && view.probability < 0.4) ||
          (batchProbability === "40to69" &&
            view.probability >= 0.4 &&
            view.probability < 0.7) ||
          (batchProbability === "70to89" &&
            view.probability >= 0.7 &&
            view.probability < 0.9) ||
          (batchProbability === "90plus" && view.probability >= 0.9);

        return riskMatch && decisionMatch && probabilityMatch;
      }),
    [
      normalizedCsvResults,
      batchRisk,
      batchDecision,
      batchProbability,
    ],
  );

  const riskDrivers = useMemo(() => {
    const candidates =
      result?.risk_drivers ??
      result?.drivers ??
      result?.top_features ??
      [];

    if (Array.isArray(candidates) && candidates.length) {
      return candidates.slice(0, 4).map((driver: any, index: number) => ({
        title:
          driver.feature ??
          driver.name ??
          `Driver ${index + 1}`,
        description:
          driver.description ??
          `Contribution: ${driver.value ?? driver.impact ?? "model signal"}`,
      }));
    }

    return [
      {
        title: `Shipping mode · ${form.shipping_mode}`,
        description:
          "Service level is part of the champion model feature set.",
      },
      {
        title: `${form.customer_city} → ${form.order_city}`,
        description:
          "Route-related location features contribute to the risk score.",
      },
      {
        title: `Order value · €${Number(form.sales).toFixed(0)}`,
        description:
          "Commercial and order characteristics are included in inference.",
      },
    ];
  }, [result, form]);

  return (
    <>
      <Header
        eyebrow="OPERATIONS · DATA INTAKE"
        title="Parcel Intake & Prediction"
        subtitle="Score a single parcel or upload a CSV batch using the active champion ML pipeline."
      />

      <div className="segmented">
        <button
          className={mode === "single" ? "active" : ""}
          onClick={() => setMode("single")}
        >
          <PackagePlus size={17} />
          Single parcel
        </button>
        <button
          className={mode === "csv" ? "active" : ""}
          onClick={() => setMode("csv")}
        >
          <FileSpreadsheet size={17} />
          CSV batch
        </button>
      </div>

      {mode === "single" ? (
        <div className="grid2 prediction-grid">
          <Card>
            <SectionTitle
              title="Shipment details"
              subtitle="Operational fields used by the champion model"
            />

            <form onSubmit={go} className="shipment-form">
              <div className="fields">
                <label>
                  Shipment ID
                  <input
                    value={form.external_id}
                    onChange={(e) =>
                      set("external_id", e.target.value)
                    }
                  />
                </label>

                <label>
                  Shipping mode
                  <select
                    value={form.shipping_mode}
                    onChange={(e) =>
                      set("shipping_mode", e.target.value)
                    }
                  >
                    <option>Standard Class</option>
                    <option>Second Class</option>
                    <option>First Class</option>
                    <option>Same Day</option>
                  </select>
                </label>

                <label>
                  Origin city
                  <input
                    value={form.customer_city}
                    onChange={(e) =>
                      set("customer_city", e.target.value)
                    }
                  />
                </label>

                <label>
                  Destination city
                  <input
                    value={form.order_city}
                    onChange={(e) =>
                      set("order_city", e.target.value)
                    }
                  />
                </label>

                <label>
                  Country
                  <input
                    value={form.order_country}
                    onChange={(e) => {
                      set("order_country", e.target.value);
                      set("customer_country", e.target.value);
                    }}
                  />
                </label>

                <label>
                  Product category
                  <input
                    value={form.category_name}
                    onChange={(e) =>
                      set("category_name", e.target.value)
                    }
                  />
                </label>

                <label>
                  Product price
                  <input
                    type="number"
                    value={form.product_price}
                    onChange={(e) =>
                      set("product_price", Number(e.target.value))
                    }
                  />
                </label>

                <label>
                  Quantity
                  <input
                    type="number"
                    value={form.order_item_quantity}
                    onChange={(e) =>
                      set(
                        "order_item_quantity",
                        Number(e.target.value),
                      )
                    }
                  />
                </label>
              </div>

              <details>
                <summary>Advanced model fields</summary>
                <div className="fields compact">
                  <label>
                    Latitude
                    <input
                      type="number"
                      value={form.latitude}
                      onChange={(e) =>
                        set("latitude", Number(e.target.value))
                      }
                    />
                  </label>
                  <label>
                    Longitude
                    <input
                      type="number"
                      value={form.longitude}
                      onChange={(e) =>
                        set("longitude", Number(e.target.value))
                      }
                    />
                  </label>
                  <label>
                    Sales
                    <input
                      type="number"
                      value={form.sales}
                      onChange={(e) =>
                        set("sales", Number(e.target.value))
                      }
                    />
                  </label>
                  <label>
                    Profit / order
                    <input
                      type="number"
                      value={form.profit_per_order}
                      onChange={(e) =>
                        set(
                          "profit_per_order",
                          Number(e.target.value),
                        )
                      }
                    />
                  </label>
                </div>
              </details>

              <AsyncButton
                loading={loading}
                loadingText="Scoring parcel"
                className="primary full"
                type="submit"
              >
                <WandSparkles size={17} />
                Predict delay risk
              </AsyncButton>

              {error && <div className="error">{error}</div>}
            </form>
          </Card>

          <Card className="prediction-result">
            {loading ? (
              <div className="prediction-loading">
                <div className="prediction-orbit">
                  <span />
                  <span />
                  <span />
                  <Sparkles size={25} />
                </div>
                <b>Scoring shipment</b>
                <p>
                  Applying feature engineering and the active champion
                  pipeline…
                </p>
                <div className="prediction-loading-bar">
                  <span />
                </div>
              </div>
            ) : !result ? (
              <div className="empty-state">
                <Sparkles size={45} />
                <b>No prediction yet</b>
                <p>
                  Complete the parcel details and run the champion
                  model.
                </p>
              </div>
            ) : (
              <>
                <SectionTitle
                  title="Prediction Intelligence"
                  subtitle="Model score, explanation and recommended action"
                  action={
                    <button
                      className="text-button"
                      onClick={onAsk}
                    >
                      Ask AI →
                    </button>
                  }
                />

                <div className="prediction-hero">
                  <RiskGauge probability={probability} />
                  <div>
                    <span className="prediction-label">
                      {currentPrediction?.isDelayed
                        ? "DELAY LIKELY"
                        : "ON TRACK"}
                    </span>
                    <h2>{form.external_id}</h2>
                    <p>{explanation}</p>
                  </div>
                </div>

                <div className="driver-grid">
                  {riskDrivers.map((driver) => (
                    <InsightRow
                      key={driver.title}
                      title={driver.title}
                      description={driver.description}
                    />
                  ))}
                </div>

                <HighRiskRecommendations
                  probability={probability}
                  drivers={riskDrivers.map((driver) => driver.title)}
                />
              </>
            )}
          </Card>
        </div>
      ) : (
        <>
          <Card className="csv-drop-card compact-card">
            <input
              ref={fileRef}
              hidden
              type="file"
              accept=".csv,text/csv"
              onChange={handleCsv}
            />

            <div
              className="csv-drop"
              onClick={() => fileRef.current?.click()}
            >
              <CloudUpload size={36} />
              <b>Drop operational CSV here</b>
              <p>
                Or click to choose a file. Existing shipment schema
                columns are supported.
              </p>
              <button className="secondary-inline">
                Choose CSV
              </button>
            </div>

            {csvRows.length > 0 && (
              <div className="csv-summary">
                <span>
                  <CheckCircle2 size={16} /> {csvRows.length} rows
                  validated
                </span>
                <AsyncButton
                  loading={loading}
                  loadingText={`Scoring ${batchProgress}%`}
                  className="primary"
                  onClick={runBatch}
                >
                  Run batch prediction
                </AsyncButton>
              </div>
            )}

            {loading && csvRows.length > 0 && (
              <div className="batch-progress">
                <span style={{ width: `${batchProgress}%` }} />
              </div>
            )}
          </Card>

          {csvRows.length > 0 && (
            <Card className="compact-card batch-preview-card">
              <SectionTitle
                title="Batch preview"
                subtitle="First five shipments"
              />
              <div className="premium-table">
                <div className="premium-table-head five">
                  <span>Shipment</span>
                  <span>Origin</span>
                  <span>Destination</span>
                  <span>Mode</span>
                  <span>Quantity</span>
                </div>
                {csvRows.slice(0, 5).map((row, index) => (
                  <div
                    className="premium-table-row five"
                    key={row.external_id ?? index}
                  >
                    <b>{row.external_id}</b>
                    <span>{row.customer_city}</span>
                    <span>{row.order_city}</span>
                    <span>{row.shipping_mode}</span>
                    <span>{row.order_item_quantity}</span>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {csvResults.length > 0 && (
            <Card className="compact-card batch-results-card">
              <SectionTitle
                title="Batch prediction results"
                subtitle={`${csvResults.filter((x) => x.ok).length} successful · ${
                  csvResults.filter((x) => !x.ok).length
                } failed · ${shownCsvResults.length} shown`}
                action={
                  <div className="filter-row compact-filter-row">
                    <Filter size={14} />

                    <select
                      value={batchRisk}
                      onChange={(e) => setBatchRisk(e.target.value)}
                    >
                      <option value="all">All risk</option>
                      <option value="high">High</option>
                      <option value="medium">Medium</option>
                      <option value="low">Low</option>
                    </select>

                    <select
                      value={batchDecision}
                      onChange={(e) => setBatchDecision(e.target.value)}
                    >
                      <option value="all">All results</option>
                      <option value="delay">Delay likely</option>
                      <option value="track">On track</option>
                    </select>

                    <select
                      value={batchProbability}
                      onChange={(e) => setBatchProbability(e.target.value)}
                    >
                      <option value="all">Any probability</option>
                      <option value="lt40">&lt; 40%</option>
                      <option value="40to69">40–69%</option>
                      <option value="70to89">70–89%</option>
                      <option value="90plus">90%+</option>
                    </select>
                  </div>
                }
              />

              <div className="premium-table">
                <div className="premium-table-head five">
                  <span>Shipment</span>
                  <span>Status</span>
                  <span>Risk</span>
                  <span>Probability</span>
                  <span>Prediction</span>
                </div>

                {shownCsvResults.map(({ item, index, view }) => (
                  <div
                    className="premium-table-row five"
                    key={item.external_id ?? index}
                  >
                    <b>{item.external_id}</b>

                    <span>{item.ok ? "Scored" : "Failed"}</span>

                    {view ? (
                      <RiskBadge level={view.riskLevel} />
                    ) : (
                      <span>—</span>
                    )}

                    <strong>
                      {view
                        ? `${(view.probability * 100).toFixed(1)}%`
                        : "—"}
                    </strong>

                    <span
                      className={
                        view
                          ? view.isDelayed
                            ? "prediction-decision delayed"
                            : "prediction-decision on-track"
                          : ""
                      }
                    >
                      {view ? view.decisionLabel : "Error"}
                    </span>
                  </div>
                ))}

                {!shownCsvResults.length && (
                  <div className="table-empty">
                    No batch results match these filters.
                  </div>
                )}
              </div>
            </Card>
          )}
        </>
      )}
    </>
  );
}
