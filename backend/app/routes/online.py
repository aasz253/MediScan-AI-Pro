from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.online_services import (
    OpenRouterService,
    OpenMeteoService,
    EpidataService,
    GeoapifyService,
)

router = APIRouter(prefix="/api/online", tags=["online"])


class ChatRequest(BaseModel):
    question: str
    context: Optional[str] = ""


class LocationRequest(BaseModel):
    latitude: float
    longitude: float


@router.post("/chat")
async def ai_chat(request: ChatRequest):
    service = OpenRouterService()
    result = await service.ask(request.question, request.context)
    return result


@router.get("/weather")
async def get_weather(latitude: float, longitude: float):
    service = OpenMeteoService()
    weather = await service.get_weather(latitude, longitude)
    if "error" in weather:
        raise HTTPException(status_code=502, detail=weather["error"])
    risks = service.map_weather_to_risks(weather)
    return {"weather": weather, "risk_assessment": risks}


@router.get("/outbreaks")
async def get_outbreaks(region: Optional[str] = ""):
    service = EpidataService()
    data = await service.get_outbreak_data(region)
    alerts = service.parse_alerts(data)
    return {"data": data, "alerts": alerts}


@router.get("/location")
async def get_location(lat: float, lon: float):
    service = GeoapifyService()
    result = await service.reverse_geocode(lat, lon)
    return result


@router.post("/risk-assessment")
async def full_risk_assessment(request: LocationRequest):
    weather_service = OpenMeteoService()
    epidata_service = EpidataService()
    geo_service = GeoapifyService()

    weather = await weather_service.get_weather(request.latitude, request.longitude)
    weather_risks = weather_service.map_weather_to_risks(weather) if "error" not in weather else []

    outbreak_data = await epidata_service.get_outbreak_data()
    outbreak_alerts = epidata_service.parse_alerts(outbreak_data)

    location_info = await geo_service.reverse_geocode(request.latitude, request.longitude)

    all_risks = []
    for risk in weather_risks:
        all_risks.append({
            "source": "weather",
            **risk,
        })
    for alert in outbreak_alerts:
        all_risks.append({
            "source": "outbreak",
            **alert,
        })

    return {
        "location": location_info,
        "weather": weather if "error" not in weather else None,
        "risks": all_risks,
        "smart_alerts": generate_smart_alerts(all_risks, weather),
    }


def generate_smart_alerts(risks: list, weather: dict) -> list:
    alerts = []
    risk_names = [r.get("disease", "") for r in risks]

    if "Malaria" in risk_names:
        alerts.append({
            "type": "warning",
            "message": "High malaria risk due to rainfall + regional outbreak data. Use mosquito protection.",
            "severity": "high",
        })

    if "Dengue Fever" in risk_names:
        alerts.append({
            "type": "warning",
            "message": "Dengue risk elevated. Eliminate standing water around your home.",
            "severity": "high",
        })

    if "Influenza / Common Cold" in risk_names:
        alerts.append({
            "type": "info",
            "message": "Respiratory illness risk is moderate. Practice good hygiene and consider a flu vaccine.",
            "severity": "medium",
        })

    if "Cholera" in risk_names:
        alerts.append({
            "type": "critical",
            "message": "Waterborne disease risk detected. Ensure drinking water is safe and properly treated.",
            "severity": "critical",
        })

    if not alerts and risks:
        alerts.append({
            "type": "info",
            "message": "Health risk data has been updated for your area. Review the risk assessment below.",
            "severity": "low",
        })

    return alerts
