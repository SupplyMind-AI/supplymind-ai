"""Deterministic within-batch event deduplication."""
from __future__ import annotations
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from supplymind.features.external_intelligence.domain.schemas import EventType

@dataclass
class EventCandidate:
    source_url:str;event_type:EventType;title:str;summary:str|None;severity:float;country:str|None;region:str|None;city:str|None;published_at:datetime|None;original_title:str;source_language:str|None;domain:str|None

def _normalize_title(value:str)->str:
    return " ".join(re.sub(r"[^a-z0-9\s]"," ",value.casefold()).split())

def _normalize_location(value:str|None)->str|None:
    if not value:return None
    v=re.sub(r"\b(and|the)\b"," ",value.casefold());v=re.sub(r"[^a-z0-9\s]"," ",v)
    return " ".join(sorted(v.split()))

def _title_similarity(a:str,b:str)->float:return SequenceMatcher(None,_normalize_title(a),_normalize_title(b)).ratio()

def _compatible_location(a:EventCandidate,b:EventCandidate)->bool:
    ac,bc=_normalize_location(a.country),_normalize_location(b.country)
    if ac and bc and ac!=bc:return False
    ar,br=_normalize_location(a.region),_normalize_location(b.region)
    return ar==br if ar and br else True

def _as_utc(v:datetime|None)->datetime|None:
    if v is None:return None
    if v.tzinfo is None:return v.replace(tzinfo=timezone.utc)
    return v.astimezone(timezone.utc)

def _within_window(a:datetime|None,b:datetime|None,*,window:timedelta)->bool:
    a,b=_as_utc(a),_as_utc(b)
    return True if a is None or b is None else abs(a-b)<=window

def deduplicate_events(candidates:list[EventCandidate],*,title_similarity_threshold:float=.75,publication_window_hours:int=48)->list[EventCandidate]:
    unique=[];window=timedelta(hours=publication_window_hours)
    for c in candidates:
        idx=None
        for i,e in enumerate(unique):
            same_url=bool(c.source_url and c.source_url==e.source_url)
            same_event=(c.event_type==e.event_type and _compatible_location(c,e) and _within_window(c.published_at,e.published_at,window=window) and _title_similarity(c.title,e.title)>=title_similarity_threshold)
            if same_url or same_event:idx=i;break
        if idx is None:unique.append(c);continue
        e=unique[idx];winner=c if c.severity>e.severity else e;loser=e if winner is c else c
        winner.region=winner.region or loser.region;winner.city=winner.city or loser.city;winner.country=winner.country or loser.country;winner.summary=winner.summary or loser.summary;unique[idx]=winner
    return unique
