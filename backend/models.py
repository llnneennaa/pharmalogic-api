from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class UserRole(str, enum.Enum):
    patient = "patient"
    doctor = "doctor"
    pharmacist = "pharmacist"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.patient, nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    conditions = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)  # comma-separated list


class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)

    interactions_as_drug1 = relationship(
        "Interaction", foreign_keys="Interaction.drug1_id", back_populates="drug1"
    )
    interactions_as_drug2 = relationship(
        "Interaction", foreign_keys="Interaction.drug2_id", back_populates="drug2"
    )


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    drug1_id = Column(Integer, ForeignKey("drugs.id"), nullable=False)
    drug2_id = Column(Integer, ForeignKey("drugs.id"), nullable=False)
    severity = Column(String, nullable=False)  # "high", "moderate", "low"
    description = Column(Text, nullable=False)

    drug1 = relationship("Drug", foreign_keys=[drug1_id], back_populates="interactions_as_drug1")
    drug2 = relationship("Drug", foreign_keys=[drug2_id], back_populates="interactions_as_drug2")
    lab_alerts = relationship("LabAlert", back_populates="interaction")


class LabAlert(Base):
    __tablename__ = "lab_alerts"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    alert_text = Column(Text, nullable=False)

    interaction = relationship("Interaction", back_populates="lab_alerts")