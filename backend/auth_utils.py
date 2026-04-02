"""
Standalone auth helpers — no FastAPI router imports here so any module
can import this without circular-import issues.
"""

from datetime import datetime, timedelta
from typing import Optional
import bcrypt

from fastapi import HTTPException, status
from jose import JWTError, jwt

SECRET_KEY = "pharmalogic-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """تشفير كلمة المرور باستخدام bcrypt"""
    # تحويل كلمة المرور إلى bytes
    password_bytes = password.encode('utf-8')
    # إنشاء الملح (salt) وتشفير كلمة المرور
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # إرجاع النتيجة كنص
    return hashed.decode('utf-8')


def verify_password(plain: str, hashed: str) -> bool:
    """التحقق من صحة كلمة المرور"""
    # تحويل النصوص إلى bytes
    plain_bytes = plain.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    # التحقق
    return bcrypt.checkpw(plain_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )