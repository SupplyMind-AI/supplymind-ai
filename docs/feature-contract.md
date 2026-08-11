# Delay Prediction Feature Contract

## Prediction moment

SupplyMind V1 predicts delay risk from information available at order/planning
time. The training contract therefore does not use actual shipment outcome or
fields whose value may only become available later.

## Excluded

- `label`
- `delivery_outcome`
- `shipping_date`
- `order_status`
- direct customer/order/order-item identifiers
- redundant category IDs where semantic names are retained

## Numerical features

See `domain/constants.py::NUMERICAL_FEATURES`.

## Categorical features

See `domain/constants.py::CATEGORICAL_FEATURES`.

## Encoding

Low/medium-cardinality categorical features are one-hot encoded.
High-cardinality customer/order geography is frequency encoded without the
target.

## Future enrichment

Open-Meteo weather and GDELT event features are intentionally not fabricated
inside the SynDelay-only champion. They should be joined through their own
feature adapters and included in a subsequent training run.
