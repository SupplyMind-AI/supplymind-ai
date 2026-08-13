from typing import Any,TypedDict
from supplymind.features.assistant.domain.schemas import AssistantIntent
class AssistantState(TypedDict,total=False):
 query:str;shipment_external_id:str|None;location:str|None;intent:AssistantIntent;context:list[dict[str,Any]];answer:dict[str,Any]
