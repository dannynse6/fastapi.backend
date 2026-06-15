from fastapi import Depends
from fastapi import HTTPException

from jose import jwt

from fastapi.security import OAuth2PasswordBearer

from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
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
