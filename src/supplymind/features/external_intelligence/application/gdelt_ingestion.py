from __future__ import annotations
import hashlib
from supplymind.features.events.application.use_cases import UpsertEvent
from supplymind.features.events.domain.entities import SupplyChainEvent
class IngestGdeltEvents:
    def __init__(self,*,gdelt_client,extractor,geocoder,upsert_event:UpsertEvent)->None:
        self.gdelt_client=gdelt_client; self.extractor=extractor; self.geocoder=geocoder; self.upsert_event=upsert_event
    async def execute(self)->list[SupplyChainEvent]:
        persisted=[]
        for article in await self.gdelt_client.fetch_recent():
            e=await self.extractor.extract(article)
            if not e.relevant: continue
            q=e.city or e.region or e.country; lat=lon=None
            if q:
                loc=await self.geocoder.geocode(q)
                if loc: lat,lon=loc.latitude,loc.longitude
            persisted.append(await self.upsert_event.execute(external_id=hashlib.sha256(article.url.encode()).hexdigest(),source='gdelt',event_type=e.event_type or 'other',title=e.title or article.title,description=e.description,severity=e.severity,country=e.country or article.source_country,region=e.region,latitude=lat,longitude=lon,starts_at=e.starts_at or article.seen_at,ends_at=e.ends_at,raw_payload={'article_url':article.url,'domain':article.domain,'language':article.language,'extraction_rationale':e.rationale}))
        return persisted
