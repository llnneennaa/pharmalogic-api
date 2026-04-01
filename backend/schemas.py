from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class UserRole(str, Enum):
    patient = "patient"
    doctor = "doctor"
    pharmacist = "pharmacist"


# ── Auth schemas ──────────────────────────────────────────────────────────────


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.patient
    age: Optional[int] = None
    gender: Optional[str] = None
    conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None  # comma-separated


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── User schemas ──────────────────────────────────────────────────────────────


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    age: Optional[int] = None
    gender: Optional[str] = None
    conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    conditions: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None


# ── Drug schemas ──────────────────────────────────────────────────────────────


class DrugCreate(BaseModel):
    name: str
    description: Optional[str] = None


class DrugOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# ── Interaction schemas ───────────────────────────────────────────────────────


class InteractionOut(BaseModel):
    id: int
    drug1: str
    drug2: str
    severity: str
    description: str

    class Config:
        from_attributes = True


class LabAlertOut(BaseModel):
    id: int
    alert_text: str

    class Config:
        from_attributes = True


# ── Analysis schemas ──────────────────────────────────────────────────────────


class AnalysisRequest(BaseModel):
    drugs: List[str]


class AnalysisResult(BaseModel):
    interactions: List[InteractionOut]
    risk_level: str
    risk_percentage: int = 0
    recommendation: str
    lab_alerts: List[LabAlertOut]
    allergy_warnings: List[str] = []