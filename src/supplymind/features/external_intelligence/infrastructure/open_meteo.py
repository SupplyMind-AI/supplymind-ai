"""Async Open-Meteo geocoding and forecast client."""
from __future__ import annotations
from datetime import datetime
import httpx
from supplymind.features.external_intelligence.domain.schemas import ResolvedLocation, WeatherRiskAssessment

class OpenMeteoClient:
    def __init__(self, *, geocoding_url: str, forecast_url: str, forecast_days: int = 7, timeout_seconds: float = 15.0) -> None:
        self.geocoding_url=geocoding_url; self.forecast_url=forecast_url; self.forecast_days=forecast_days; self.timeout_seconds=timeout_seconds
    async def geocode(self, location: str, *, country_code: str | None = None) -> ResolvedLocation | None:
        params={'name':location,'count':1,'language':'en','format':'json'}
        if country_code: params['countryCode']=country_code.upper()
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            r=await client.get(self.geocoding_url,params=params); r.raise_for_status(); data=r.json()
        items=data.get('results') or []
        if not items: return None
        x=items[0]
        return ResolvedLocation(name=x['name'],country=x.get('country'),country_code=x.get('country_code'),region=x.get('admin1'),latitude=float(x['latitude']),longitude=float(x['longitude']),timezone=x.get('timezone'))
    async def weather_risk(self, location: ResolvedLocation) -> WeatherRiskAssessment:
        params={'latitude':location.latitude,'longitude':location.longitude,'timezone':'auto','forecast_days':self.forecast_days,'hourly':'precipitation_probability,precipitation,snowfall,visibility,wind_gusts_10m,weather_code,temperature_2m'}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            r=await client.get(self.forecast_url,params=params); r.raise_for_status(); data=r.json()
        h=data.get('hourly') or {}
        vals=lambda k:[float(v) for v in (h.get(k) or []) if v is not None]
        pp,pr,sn,vi,wg=vals('precipitation_probability'),vals('precipitation'),vals('snowfall'),vals('visibility'),vals('wind_gusts_10m')
        mpp=max(pp) if pp else None; mw=max(wg) if wg else None; tp=sum(pr) if pr else None; ts=sum(sn) if sn else None; mv=min(vi) if vi else None
        score=0.0; reasons=[]
        if mpp is not None and mpp>=70: score+=.25; reasons.append(f'High precipitation probability ({mpp:.0f}%).')
        if tp is not None and tp>=30: score+=.25; reasons.append(f'Heavy accumulated precipitation ({tp:.1f} mm).')
        if ts is not None and ts>=5: score+=.25; reasons.append(f'Meaningful snowfall forecast ({ts:.1f} cm).')
        if mw is not None and mw>=60: score+=.25; reasons.append(f'Strong wind gusts ({mw:.0f} km/h).')
        if mv is not None and mv<=1000: score+=.15; reasons.append(f'Low visibility ({mv:.0f} m).')
        score=min(score,1.0); level='high' if score>=.65 else 'medium' if score>=.30 else 'low'; times=h.get('time') or []
        parse=lambda s: datetime.fromisoformat(s) if s else None
        return WeatherRiskAssessment(location=location,risk_level=level,risk_score=score,max_precipitation_probability=mpp,max_wind_gust_kmh=mw,total_precipitation_mm=tp,total_snowfall_cm=ts,minimum_visibility_m=mv,reasons=reasons,forecast_start=parse(times[0]) if times else None,forecast_end=parse(times[-1]) if times else None)
