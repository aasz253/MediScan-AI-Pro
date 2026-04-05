from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app.services.offline_engine import OfflineEngine

router = APIRouter(prefix="/api", tags=["offline"])


class SymptomMatchRequest(BaseModel):
    symptom_ids: List[int]
    top_n: Optional[int] = 5


class SearchRequest(BaseModel):
    query: str


@router.get("/symptoms")
def get_all_symptoms(db: Session = Depends(get_db)):
    engine = OfflineEngine(db)
    return {"symptoms": engine.get_all_symptoms()}


@router.get("/diseases")
def get_all_diseases(db: Session = Depends(get_db)):
    engine = OfflineEngine(db)
    return {"diseases": engine.get_all_diseases()}


@router.get("/diseases/search")
def search_diseases(q: str, db: Session = Depends(get_db)):
    engine = OfflineEngine(db)
    if not q or len(q) < 2:
        return {"diseases": []}
    return {"diseases": engine.search_diseases(q)}


@router.post("/match")
def match_diseases(request: SymptomMatchRequest, db: Session = Depends(get_db)):
    engine = OfflineEngine(db)
    results = engine.match_diseases(request.symptom_ids, request.top_n)
    return {"results": results, "count": len(results), "mode": "offline"}


@router.get("/disease/{disease_id}")
def get_disease_detail(disease_id: int, db: Session = Depends(get_db)):
    engine = OfflineEngine(db)
    all_diseases = engine.get_all_diseases()
    for d in all_diseases:
        if d["id"] == disease_id:
            return {"disease": d}
    raise HTTPException(status_code=404, detail="Disease not found")
