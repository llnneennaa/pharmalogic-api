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
from typing import Optional

router = APIRouter(prefix="/users", tags=["users"])
bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
    db: Session = Depends(get_db),
) -> Optional[models.User]:
    """Get current user from JWT token, returns None if not authenticated"""
    
    # إذا لم يكن هناك توكن، نرجع None (مستخدم زائر/ضيف)
    if not credentials:
        return None
    
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = db.query(models.User).filter(models.User.id == int(user_id)).first()
        return user
    except Exception:
        # إذا كان التوكن غير صالح، نعامل المستخدم كزائر
        return None


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