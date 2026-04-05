"""
Drugs router: GET /drugs, POST /drugs
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from routers.users import get_current_user, require_role
from drug_info_data import (
    get_common_uses, get_side_effects, get_contraindications,
    get_vitamin_depletions, get_pregnancy_safety,
    get_counseling_points, get_references
)

router = APIRouter(prefix="/drugs", tags=["drugs"])


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("", response_model=List[schemas.DrugOut])
def list_drugs(db: Session = Depends(get_db)):
    """Public endpoint – anyone can list available drugs."""
    return db.query(models.Drug).order_by(models.Drug.name).all()


@router.post("", response_model=schemas.DrugOut, status_code=201)
def create_drug(
    payload: schemas.DrugCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("doctor", "pharmacist")),
):
    """Only doctors and pharmacists can add drugs."""
    existing = db.query(models.Drug).filter(models.Drug.name.ilike(payload.name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Drug already exists")

    drug = models.Drug(name=payload.name, description=payload.description)
    db.add(drug)
    db.commit()
    db.refresh(drug)
    return drug


@router.get("/{drug_id}", response_model=schemas.DrugOut)
def get_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = db.query(models.Drug).filter(models.Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug
@router.get("/{drug_id}/detailed", response_model=schemas.DrugDetailedOut)
def get_drug_detailed(drug_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific drug for Medical Team reference
    """
    drug = db.query(models.Drug).filter(models.Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    # Get interactions for this drug
    interactions = []
    
    # Interactions where this drug is drug1
    for interaction in drug.interactions_as_drug1:
        interactions.append({
            "drug": interaction.drug2.name,
            "severity": interaction.severity,
            "description": interaction.description
        })
    
    # Interactions where this drug is drug2
    for interaction in drug.interactions_as_drug2:
        interactions.append({
            "drug": interaction.drug1.name,
            "severity": interaction.severity,
            "description": interaction.description
        })
    
    return {
        "id": drug.id,
        "name": drug.name,
        "description": drug.description or "",
        "common_uses": get_common_uses(drug.name),
        "side_effects": get_side_effects(drug.name),
        "contraindications": get_contraindications(drug.name),
        "interactions": interactions,
        "vitamin_depletions": get_vitamin_depletions(drug.name),
        "pregnancy_safety": get_pregnancy_safety(drug.name),
        "counseling_points": get_counseling_points(drug.name),
        "references": get_references(drug.name)
    }