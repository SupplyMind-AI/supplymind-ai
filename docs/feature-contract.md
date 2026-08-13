# Delay Prediction Feature Contract

## Prediction moment

SupplyMind V1 predicts delay risk from information available at order/planning
time. The model cannot use actual shipment outcome or fields whose value may only
become available later.

## Raw source versus canonical dataset

The raw SynDelay v1 file contains 41 columns and `label` as the multiclass source
target. Canonicalization adds:

- `delivery_outcome` — preserved source label for provenance
- `is_delayed` — V1 binary target

These target columns are never model inputs.

## Excluded fields

- `label`
- `delivery_outcome`
- `is_delayed`
- `shipping_date`
- `order_status`
- direct customer/order/order-item identifiers
- redundant category IDs where semantic names are retained
- `customer_zipcode`

## Feature engineering

`order_date` produces calendar features such as month, weekday, hour, and weekend.
High-cardinality city/state fields are frequency encoded with mappings learned
only from the training partition and persisted with the model.

## Numerical features

See `domain/constants.py::NUMERICAL_FEATURES`.

## Categorical features

See `domain/constants.py::CATEGORICAL_FEATURES`.

## Encoding

Low/medium-cardinality categorical fields are one-hot encoded. Numerical fields
are median-imputed and scaled only when required by the estimator.

## Future enrichment

Open-Meteo weather and GDELT event features are not fabricated in the SynDelay-only
baseline. They will be joined through dedicated feature adapters and included in a
later retraining run.
