import re
_WEATHER=re.compile(r'\b(weather|rain|snow|storm|wind|forecast|temperature|visibility)\b',re.I)
_EVENTS=re.compile(r'\b(event|disruption|strike|port|conflict|flood|wildfire|gdelt|news)\b',re.I)
_KNOWLEDGE=re.compile(r'\b(document|policy|catalog|manual|procedure|sop|knowledge|semantic)\b',re.I)
_COMBINED=re.compile(r'\b(why|explain|risk|reason|context|arrive|delay|delayed)\b',re.I)
def route_query(query:str,*,shipment_external_id:str|None=None,location:str|None=None):
 if shipment_external_id and _COMBINED.search(query): return 'combined'
 if location and _WEATHER.search(query): return 'weather'
 if _EVENTS.search(query): return 'events'
 if _KNOWLEDGE.search(query): return 'knowledge'
 if shipment_external_id:return 'shipment'
 return 'knowledge'
