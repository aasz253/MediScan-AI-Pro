from sqlalchemy.orm import Session
from app.models.models import Disease, Symptom, disease_symptoms
from typing import List, Dict, Any


class OfflineEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_all_symptoms(self) -> List[Dict[str, Any]]:
        symptoms = self.db.query(Symptom).order_by(Symptom.name).all()
        return [{"id": s.id, "name": s.name} for s in symptoms]

    def get_all_diseases(self) -> List[Dict[str, Any]]:
        diseases = self.db.query(Disease).all()
        results = []
        for d in diseases:
            results.append({
                "id": d.id,
                "name": d.name,
                "description": d.description or "",
                "causes": d.causes or "",
                "prevention": d.prevention or "",
                "symptoms": [s.name for s in d.symptoms],
                "treatment": {
                    "immediate_action": d.treatments.immediate_action if d.treatments else "",
                    "medications": d.treatments.medications if d.treatments else "",
                } if d.treatments else {"immediate_action": "", "medications": ""}
            })
        return results

    def search_diseases(self, query: str) -> List[Dict[str, Any]]:
        diseases = self.db.query(Disease).filter(
            Disease.name.ilike(f"%{query}%")
        ).all()
        results = []
        for d in diseases:
            results.append({
                "id": d.id,
                "name": d.name,
                "description": d.description or "",
                "causes": d.causes or "",
                "prevention": d.prevention or "",
                "symptoms": [s.name for s in d.symptoms],
            })
        return results

    def match_diseases(self, symptom_ids: List[int], top_n: int = 5) -> List[Dict[str, Any]]:
        if not symptom_ids:
            return []

        diseases = self.db.query(Disease).all()
        scored = []

        for disease in diseases:
            disease_symptom_ids = [s.id for s in disease.symptoms]
            if not disease_symptom_ids:
                continue

            matched = set(symptom_ids) & set(disease_symptom_ids)
            if not matched:
                continue

            match_percentage = round((len(matched) / len(disease_symptom_ids)) * 100, 1)

            matched_names = []
            for sid in matched:
                sym = self.db.query(Symptom).filter(Symptom.id == sid).first()
                if sym:
                    matched_names.append(sym.name)

            scored.append({
                "id": disease.id,
                "name": disease.name,
                "match_percentage": match_percentage,
                "matched_symptoms": matched_names,
                "total_symptoms": len(disease_symptom_ids),
                "matched_count": len(matched),
                "description": disease.description or "",
                "causes": disease.causes or "",
                "prevention": disease.prevention or "",
                "all_symptoms": [s.name for s in disease.symptoms],
                "immediate_action": disease.treatments.immediate_action if disease.treatments else "",
                "medications": disease.treatments.medications if disease.treatments else "",
            })

        scored.sort(key=lambda x: x["match_percentage"], reverse=True)
        return scored[:top_n]
