from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import models
import schemas
import crud
import auth

from database import get_db


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================
# Register
# ==========================

@router.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = crud.get_user_by_username(
        db,
        user.username
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    hashed_password = auth.hash_password(
        user.password
    )


    new_user = models.User(
        username=user.username,
        password=hashed_password,
        role=user.role
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message": "User Registered Successfully",
        "username": new_user.username,
        "role": new_user.role
    }



# ==========================
# Login
# ==========================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.get_user_by_username(
        db,
        form_data.username
    )


    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    if not auth.verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )


    token = auth.create_access_token(
        {
            "username": db_user.username,
            "role": db_user.role
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }