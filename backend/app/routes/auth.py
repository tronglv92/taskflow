"""Authentication endpoints. Mounted at /api/auth."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas
from api.deps import get_db
from services import auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check first so a duplicate email becomes a clear client error, rather
    # than leaking a lower-level database uniqueness exception.
    if auth_service.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return auth_service.create_user(db, user_in)


@router.post("/token", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2's password flow is form-encoded and calls the email ``username``;
    # it is intentionally not a JSON request body.
    user = auth_service.authenticate_user(
        db, form_data.username, form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_service.create_access_token(subject=user.email)
    return schemas.Token(access_token=token)
