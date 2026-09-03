"""Shared FastAPI dependencies."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import models
from database import get_db
from services import auth_service

# get_db is re-exported so routes can import both deps from one place.
__all__ = ["get_db", "get_current_user", "oauth2_scheme"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = auth_service.decode_token(token)
    if token_data is None or token_data.email is None:
        raise credentials_error
    user = auth_service.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_error
    return user
