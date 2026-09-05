"""Authentication business logic: password hashing and JWT handling."""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
import schemas
from core.config import settings

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # bcrypt is deliberately one-way; only the resulting hash belongs in the DB.
    return _pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    # The password library performs the salted-hash comparison safely.
    return _pwd_context.verify(plain, hashed)


def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    """Sign a short-lived JWT whose subject is the user's email address."""
    minutes = expires_minutes or settings.access_token_expire_minutes
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    # ``sub`` is the standard JWT subject claim; ``exp`` makes a stolen token
    # expire rather than remain valid indefinitely.
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> Optional[schemas.TokenData]:
    """Verify signature and expiry, returning None for every invalid token."""
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
    except JWTError:
        return None
    email = payload.get("sub")
    if email is None:
        return None
    return schemas.TokenData(email=email)


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    # Never pass the plaintext password to the model; persist only its bcrypt hash.
    user = models.User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(
    db: Session, email: str, password: str
) -> Optional[models.User]:
    # Returning one generic failure avoids revealing whether an email exists.
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user
