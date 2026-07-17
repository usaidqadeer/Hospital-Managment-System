from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer



SECRET_KEY = "hospital_secret_key_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)



# ==========================
# Password Hashing
# ==========================

def hash_password(password: str):

    return pwd_context.hash(password)



def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )



# ==========================
# Create JWT Token
# ==========================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire
        }
    )


    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return encoded_jwt



# ==========================
# Verify Token
# ==========================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        username = payload.get("username")
        role = payload.get("role")


        if username is None:
            return None


        return {
            "username": username,
            "role": role
        }


    except JWTError:

        return None



# ==========================
# Get Current User
# ==========================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    user = verify_token(token)


    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


    return user



# ==========================
# Role Checker
# ==========================

def check_role(
    current_user,
    required_role
):

    if current_user["role"] != required_role:

        raise HTTPException(
            status_code=403,
            detail="You don't have permission"
        )


    return True