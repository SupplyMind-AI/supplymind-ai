"""GDELT DOC client with disruption-focused query and conservative rate-limit handling."""
from __future__ import annotations
import asyncio
from datetime import datetime
import httpx
from supplymind.features.external_intelligence.domain.schemas import GdeltArticle

DEFAULT_DISRUPTION_QUERY='("port congestion" OR "port closure" OR "shipping disruption" OR "freight disruption" OR "cargo disruption" OR "logistics disruption" OR "border closure" OR "rail disruption" OR "transport strike" OR "port strike" OR blockade OR flooding OR typhoon OR wildfire)'

def _parse_seen_at(value):
    if not value:return None
    for fmt in ("%Y%m%dT%H%M%SZ","%Y%m%d%H%M%S"):
        try:return datetime.strptime(value,fmt)
        except ValueError:pass
    return None

class GdeltClient:
    def __init__(self,*,base_url,query=None,timespan="24h",max_records=50,timeout_seconds=15.0,max_retries=4,retry_wait_seconds=5.0):
        self.base_url=base_url;self.query=query or DEFAULT_DISRUPTION_QUERY;self.timespan=timespan;self.max_records=max_records;self.timeout_seconds=timeout_seconds;self.max_retries=max_retries;self.retry_wait_seconds=max(retry_wait_seconds,5.0)
    async def fetch_recent(self):
        params={"query":self.query,"mode":"ArtList","format":"json","sort":"HybridRel","timespan":self.timespan,"maxrecords":self.max_records}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            for attempt in range(1,self.max_retries+1):
                print(f"GDELT request attempt {attempt}/{self.max_retries}...")
                try:r=await client.get(self.base_url,params=params)
                except httpx.TimeoutException:
                    if attempt==self.max_retries:raise RuntimeError("GDELT request timed out")
                    await asyncio.sleep(self.retry_wait_seconds);continue
                if r.status_code==429:
                    if attempt==self.max_retries:raise RuntimeError("GDELT rate limit remained active")
                    wait=self.retry_wait_seconds
                    try:wait=max(wait,float(r.headers.get("Retry-After",wait)))
                    except ValueError:pass
                    print(f"GDELT rate limit reached. Retrying in {wait:.0f}s...");await asyncio.sleep(wait);continue
                r.raise_for_status();data=r.json();return [GdeltArticle(url=i["url"],title=i["title"],domain=i.get("domain"),source_country=i.get("sourcecountry"),language=i.get("language"),seen_at=_parse_seen_at(i.get("seendate"))) for i in data.get("articles",[]) if i.get("url") and i.get("title")]
        return []
