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
