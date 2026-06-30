from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def hash_password(password: str):
    if len(password.encode("utf-8")) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")

    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(
        password,
        hashed_password,
    )


def create_access_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(timezone.utc)
        + timedelta(hours=1),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        return payload

    except Exception:
        raise HTTPException(401)


def require_roles(*roles):
    def checker(
        current_user=Depends(
            get_current_user
        ),
    ):
        if current_user["role"] not in roles:
            raise HTTPException(
                status_code=403,
                detail="Forbidden",
            )

        return current_user

    return checker