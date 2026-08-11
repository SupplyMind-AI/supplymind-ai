# SupplyMind ML Methodology

## Reference methodology

The analysis structure is inspired by the public `Delivery_Risk_Prediction.ipynb`
project by Polina Burova: business framing, exploratory analysis, feature
engineering, statistical feature analysis, Logistic Regression, Random Forest,
XGBoost, feature importance, and model comparison.

SupplyMind does not copy the reference implementation. It adapts the methodology
to SynDelay and the RFC's production constraints.

## Important differences

1. **Target** — SynDelay's source label is multiclass. SupplyMind V1 preserves
   `delivery_outcome` and creates `is_delayed`:
   - 0 early -> 0 not delayed
   - 1 on-time -> 0 not delayed
   - 2 delayed -> 1 delayed

2. **Temporal evaluation** — the reference notebook uses a random train/test
   split. SupplyMind uses chronological train/validation/test partitions based on
   `order_date`.

3. **Leakage policy** — `shipping_date` and `order_status` are excluded from V1
   model inputs because the model is defined at order/planning time and those
   fields are post-prediction or temporally ambiguous.

4. **High-cardinality variables** — IDs are removed. Selected high-cardinality
   locations use frequency encoding learned on the training partition only.

5. **One-hot encoding** — stable categorical business variables use
   `OneHotEncoder(handle_unknown="ignore")` inside the persisted sklearn pipeline.

6. **Training-serving consistency** — preprocessing and the estimator are saved
   together. FastAPI must load the persisted champion pipeline rather than
   recreating transformations.

7. **Champion selection** — candidates are compared on validation F1, then recall,
   then ROC-AUC. The test partition is evaluated once after selection.
