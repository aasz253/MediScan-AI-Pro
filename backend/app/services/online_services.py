import httpx
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()


class OpenRouterService:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.api_url = os.getenv("OPENROUTER_API_URL", "https://openrouter.ai/api/v1/chat/completions")
        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

    async def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_openrouter_api_key_here")

    async def ask(self, question: str, context: str = "") -> Dict[str, Any]:
        if not await self.is_available():
            return {"error": "OpenRouter API not configured", "available": False}

        system_prompt = (
            "You are a helpful medical information assistant. You provide general health information only. "
            "ALWAYS include this disclaimer at the start of every response: "
            "'DISCLAIMER: This is NOT medical diagnosis. Always consult a licensed medical professional.' "
            "Answer in simple, clear language. Never prescribe medication. "
            "Never provide certainty. Always suggest consulting a doctor."
        )

        user_message = f"Context: {context}\n\nQuestion: {question}" if context else question

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://mediscan-ai.local",
                        "X-Title": "MediScan AI Pro",
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message},
                        ],
                        "max_tokens": 1024,
                        "temperature": 0.7,
                    },
                )
                data = response.json()
                if "choices" in data:
                    return {
                        "answer": data["choices"][0]["message"]["content"],
                        "available": True,
                    }
                return {"error": str(data), "available": True}
        except Exception as e:
            return {"error": str(e), "available": True}


class OpenMeteoService:
    def __init__(self):
        self.base_url = os.getenv("OPEN_METEO_URL", "https://api.open-meteo.com/v1/forecast")

    async def get_weather(self, latitude: float, longitude: float) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    self.base_url,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": "temperature_2m,relative_humidity_2m,precipitation,weather_code",
                        "daily": "temperature_2m_max,precipitation_sum",
                        "timezone": "auto",
                    },
                )
                return response.json()
        except Exception as e:
            return {"error": str(e)}

    def map_weather_to_risks(self, weather_data: Dict[str, Any]) -> list:
        risks = []
        current = weather_data.get("current", {})

        temp = current.get("temperature_2m", 25)
        humidity = current.get("relative_humidity_2m", 50)
        precipitation = current.get("precipitation", 0)

        if humidity > 70 and precipitation > 5:
            risks.append({
                "disease": "Malaria",
                "risk_level": "High",
                "reason": "High humidity and rainfall create mosquito breeding conditions",
            })
        elif humidity > 60 and temp < 20:
            risks.append({
                "disease": "Influenza / Common Cold",
                "risk_level": "Medium",
                "reason": "Cool and humid conditions favor respiratory virus transmission",
            })

        if temp > 35:
            risks.append({
                "disease": "Heat Stroke / Dehydration",
                "risk_level": "High",
                "reason": "Extreme heat increases risk of heat-related illnesses",
            })

        if precipitation > 20:
            risks.append({
                "disease": "Dengue Fever",
                "risk_level": "Medium",
                "reason": "Heavy rainfall creates standing water for mosquito breeding",
            })
            risks.append({
                "disease": "Cholera",
                "risk_level": "Medium",
                "reason": "Heavy rainfall can contaminate water sources",
            })

        return risks


class EpidataService:
    def __init__(self):
        self.base_url = os.getenv("EPIDATA_URL", "https://delphi.cmu.edu/epidata/api.php")

    async def get_outbreak_data(self, region: str = "") -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                params = {"endpoint": "nidss_flu", "regions": region or "all"}
                response = await client.get(self.base_url, params=params)
                data = response.json()
                return data
        except Exception as e:
            return {"error": str(e)}

    def parse_alerts(self, data: Dict[str, Any]) -> list:
        alerts = []
        if "epidata" not in data or not data["epidata"]:
            return alerts

        for entry in data.get("epidata", [])[:10]:
            ilinc = entry.get("ilinc", 0)
            if ilinc > 5:
                alerts.append({
                    "disease": "Influenza-like Illness",
                    "risk_level": "High",
                    "region": entry.get("region", "Unknown"),
                    "value": ilinc,
                    "message": f"Elevated ILI activity detected in {entry.get('region', 'your region')}",
                })
            elif ilinc > 2:
                alerts.append({
                    "disease": "Influenza-like Illness",
                    "risk_level": "Medium",
                    "region": entry.get("region", "Unknown"),
                    "value": ilinc,
                    "message": f"Moderate ILI activity in {entry.get('region', 'your region')}",
                })

        return alerts


class GeoapifyService:
    def __init__(self):
        self.api_key = os.getenv("GEOAPIFY_API_KEY", "")
        self.base_url = os.getenv("GEOAPIFY_URL", "https://api.geoapify.com/v1/geocode")

    async def is_available(self) -> bool:
        return bool(self.api_key and self.api_key != "your_geoapify_api_key_here")

    async def reverse_geocode(self, lat: float, lon: float) -> Dict[str, Any]:
        if not await self.is_available():
            return {"error": "Geoapify API not configured", "available": False}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/reverse",
                    params={
                        "lat": lat,
                        "lon": lon,
                        "apiKey": self.api_key,
                        "format": "json",
                    },
                )
                data = response.json()
                return {"available": True, "data": data}
        except Exception as e:
            return {"error": str(e), "available": True}
