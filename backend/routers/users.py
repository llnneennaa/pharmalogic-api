"""
Users router: /me (get & update current user)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from auth_utils import decode_token

router = APIRouter(prefix="/users", tags=["users"])
bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> models.User:
    """Get current user from JWT token"""
    payload = decode_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_role(*roles: str):
    """Dependency to require specific user roles"""
    def dependency(current_user: models.User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(roles)}",
            )
        return current_user
    return dependency


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=schemas.UserOut)
def update_me(
    payload: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update current user profile"""
    if payload.name is not None:
        current_user.name = payload.name
    if payload.age is not None:
        current_user.age = payload.age
    if payload.gender is not None:
        current_user.gender = payload.gender
    if payload.conditions is not None:
        current_user.conditions = payload.conditions
    if payload.allergies is not None:
        current_user.allergies = payload.allergies
    if payload.medications is not None:
        current_user.medications = payload.medications

    db.commit()
    db.refresh(current_user)
    return current_user