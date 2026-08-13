# SupplyMind ML Methodology

## Target

The downloaded SynDelay v1 CSV contains **41 raw columns** and one source target,
`label`:

- `0` = early delivery
- `1` = on-time delivery
- `2` = delayed delivery

SupplyMind preserves the source outcome as `delivery_outcome` and creates the V1
binary target `is_delayed` during canonicalization:

- source classes `0` and `1` -> `is_delayed = 0`
- source class `2` -> `is_delayed = 1`

The raw CSV is never modified. The two additional target columns belong to the
SupplyMind canonical training dataset.

## Evaluation

SupplyMind uses a chronological 70/15/15 train/validation/test split based on
`order_date`. Candidate models are fitted only on the earliest training period,
compared on the middle validation period, and the selected champion is evaluated
once on the latest test period.

## Leakage policy

`shipping_date` and `order_status` are excluded from V1 model inputs because the
model is defined at order/planning time and their prediction-time availability is
post-event or ambiguous. Target-derived columns and entity identifiers are also
excluded.

## Feature engineering

Calendar features are derived from `order_date`. High-cardinality geography
(`customer_city`, `order_city`, `order_state`) is frequency encoded. Crucially,
those frequency maps are learned on training data and persisted inside the sklearn
model pipeline so validation, test, retraining, and FastAPI inference reuse the
same mappings.

## Preprocessing

Stable categorical business variables use
`OneHotEncoder(handle_unknown="ignore")`. Numerical variables are median-imputed
and scaled for estimators that benefit from standardization. Feature engineering,
preprocessing, and the estimator are persisted together as one `joblib` artifact.

## Candidate models

SupplyMind V1 compares:

1. Logistic Regression
2. Random Forest
3. XGBoost
4. HistGradientBoosting (optional in the RFC, included in the implementation)

## Champion selection

Candidates are ranked on validation F1, then delayed-class recall, then ROC-AUC.
The test set is not used for model choice or threshold tuning. After selection,
the champion is refitted on train + validation and evaluated once on test data.

## Production boundary

FastAPI must load `models/champion/model.joblib`. Serving code must not recreate
frequency mappings, one-hot encoders, scalers, or other training transformations.
