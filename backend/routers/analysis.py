from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from rules_engine import analyze_drugs
from schemas import AnalysisRequest, AnalysisResult, InteractionOut, LabAlertOut
from routers.users import get_current_user
import models

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResult)
def analyze(
    request: AnalysisRequest, 
    db: Session = Depends(get_db),
    current_user: Optional[models.User] = Depends(get_current_user)
):
    """
    Analyze drug interactions for a list of medications
    """
    print("=" * 50)
    print("🔍 ANALYZE REQUEST RECEIVED")
    print(f"🔍 Drugs: {request.drugs}")
    if current_user:
        print(f"🔍 Current user: {current_user.email}")
        print(f"🔍 User allergies: {current_user.allergies}")
    else:
        print("🔍 No user authenticated (guest mode)")
    print("=" * 50)
    
    # تمرير المستخدم الحالي إلى analyze_drugs
    result = analyze_drugs(db, request.drugs, current_user)
    
    print(f"🔍 Result keys: {result.keys()}")
    print(f"🔍 Allergy warnings in result: {result.get('allergy_warnings', [])}")
    print("=" * 50)
    
    # تحويل النتيجة إلى الشكل المطلوب في schema
    interactions_out = []
    for idx, interaction in enumerate(result["interactions"]):
        interactions_out.append(
            InteractionOut(
                id=idx + 1,
                drug1=interaction["drug1"],
                drug2=interaction["drug2"],
                severity=interaction["severity"],
                description=interaction["description"]
            )
        )
    
    lab_alerts_out = []
    for alert in result.get("lab_alerts", []):
        lab_alerts_out.append(
            LabAlertOut(
                id=alert.get("id", 0),
                alert_text=alert["alert_text"]
            )
        )
    
    return {
        "interactions": interactions_out,
        "risk_level": result["risk_level"],
        "risk_percentage": result.get("risk_percentage", 0),
        "recommendation": result["recommendation"],
        "lab_alerts": lab_alerts_out,
        "allergy_warnings": result.get("allergy_warnings", [])
    }


@router.get("/analyze/me", response_model=AnalysisResult)
def analyze_my_drugs(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze interactions for the current user's medications
    """
    print("=" * 50)
    print("🔍 ANALYZE ME REQUEST RECEIVED")
    print(f"🔍 Current user: {current_user.email}")
    print(f"🔍 User allergies: {current_user.allergies}")
    print("=" * 50)
    
    if not current_user.medications:
        return {
            "interactions": [],
            "risk_level": "none",
            "risk_percentage": 0,
            "recommendation": "No medications found in your profile. Please add medications first.",
            "lab_alerts": [],
            "allergy_warnings": []
        }
    
    # تقسيم الأدوية من النص
    drugs = [drug.strip() for drug in current_user.medications.split(",") if drug.strip()]
    
    print(f"🔍 Drugs from profile: {drugs}")
    
    result = analyze_drugs(db, drugs, current_user)
    
    print(f"🔍 Allergy warnings in result: {result.get('allergy_warnings', [])}")
    
    # تحويل النتيجة إلى الشكل المطلوب في schema
    interactions_out = []
    for idx, interaction in enumerate(result["interactions"]):
        interactions_out.append(
            InteractionOut(
                id=idx + 1,
                drug1=interaction["drug1"],
                drug2=interaction["drug2"],
                severity=interaction["severity"],
                description=interaction["description"]
            )
        )
    
    lab_alerts_out = []
    for alert in result.get("lab_alerts", []):
        lab_alerts_out.append(
            LabAlertOut(
                id=alert.get("id", 0),
                alert_text=alert["alert_text"]
            )
        )
    
    return {
        "interactions": interactions_out,
        "risk_level": result["risk_level"],
        "risk_percentage": result.get("risk_percentage", 0),
        "recommendation": result["recommendation"],
        "lab_alerts": lab_alerts_out,
        "allergy_warnings": result.get("allergy_warnings", [])
    }