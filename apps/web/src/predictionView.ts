export type RiskLevel = "low" | "medium" | "high";

export type PredictionView = {
  id: string;
  shipmentId: string;
  probability: number;
  threshold: number;
  riskLevel: RiskLevel;
  isDelayed: boolean;
  decisionLabel: "Delay likely" | "On track";
  origin: string | null;
  destination: string | null;
  shippingMode: string | null;
  raw: any;
};

function normalizeProbability(value: unknown): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return 0;
  return parsed > 1 ? parsed / 100 : parsed;
}

function readField(prediction: any, ...keys: string[]): unknown {
  const containers = [
    prediction,
    prediction?.features,
    prediction?.shipment,
    prediction?.shipment?.features,
    prediction?.shipment?.payload,
    prediction?.payload,
    prediction?.input_features,
    prediction?.metadata,
  ];

  for (const container of containers) {
    if (!container) continue;
    for (const key of keys) {
      const value = container[key];
      if (value !== undefined && value !== null && value !== "") return value;
    }
  }

  return null;
}

export function predictionView(prediction: any): PredictionView {
  const probability = normalizeProbability(
    prediction?.delay_probability ??
      prediction?.probability ??
      prediction?.risk_score ??
      prediction?.score,
  );

  const threshold = normalizeProbability(
    prediction?.threshold ??
      prediction?.model_threshold ??
      prediction?.metadata?.threshold ??
      0.62,
  );

  let isDelayed: boolean;
  if (typeof prediction?.delayed === "boolean") {
    isDelayed = prediction.delayed;
  } else if (typeof prediction?.is_delayed === "boolean") {
    isDelayed = prediction.is_delayed;
  } else if (typeof prediction?.predicted_delay === "boolean") {
    isDelayed = prediction.predicted_delay;
  } else if (prediction?.prediction === 0 || prediction?.prediction === 1) {
    isDelayed = prediction.prediction === 1;
  } else {
    // Missing boolean must never silently become "On track".
    isDelayed = probability >= threshold;
  }

  const suppliedRisk = String(prediction?.risk_level ?? "").toLowerCase();
  const riskLevel: RiskLevel =
    suppliedRisk === "high" || suppliedRisk === "medium" || suppliedRisk === "low"
      ? (suppliedRisk as RiskLevel)
      : probability >= 0.7
        ? "high"
        : probability >= 0.4
          ? "medium"
          : "low";

  const origin = readField(prediction, "origin_city", "customer_city");
  const destination = readField(prediction, "destination_city", "order_city");
  const shippingMode = readField(prediction, "shipping_mode");

  return {
    id: String(
      prediction?.prediction_id ??
        prediction?.id ??
        prediction?.shipment_id ??
        prediction?.external_id ??
        "",
    ),
    shipmentId: String(
      prediction?.external_id ??
        prediction?.shipment?.external_id ??
        prediction?.shipment_external_id ??
        prediction?.shipment_id ??
        prediction?.id ??
        "—",
    ),
    probability,
    threshold,
    riskLevel,
    isDelayed,
    decisionLabel: isDelayed ? "Delay likely" : "On track",
    origin: typeof origin === "string" ? origin : null,
    destination: typeof destination === "string" ? destination : null,
    shippingMode: typeof shippingMode === "string" ? shippingMode : null,
    raw: prediction,
  };
}
