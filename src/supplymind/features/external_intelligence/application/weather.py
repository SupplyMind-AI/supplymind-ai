from supplymind.features.external_intelligence.infrastructure.open_meteo import OpenMeteoClient
class GetWeatherRisk:
    def __init__(self, client: OpenMeteoClient)->None: self.client=client
    async def execute(self, *, location: str, country_code: str|None=None):
        resolved=await self.client.geocode(location,country_code=country_code)
        if resolved is None: raise LookupError(f'Location could not be resolved: {location}')
        return await self.client.weather_risk(resolved)
