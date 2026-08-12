from pydantic import BaseModel
class DashboardSummary(BaseModel):
 shipment_count:int;prediction_count:int;delayed_prediction_rate:float;average_delay_probability:float;active_event_count:int;queued_retraining_jobs:int;champion_model_name:str|None=None;champion_model_version:str|None=None
