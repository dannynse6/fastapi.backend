from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.session import get_db

from modules.auth.application.schemas import (
    LoginRequest,
    TokenResponse,
)

from modules.auth.application.usecases import (
    LoginUseCase,
)

from modules.user.infrastructure.repositories import (
    SQLAlchemyUserRepository,
)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)

    token = LoginUseCase(repo).execute(
        request.email,
        request.password,
    )

    return TokenResponse(
        access_token=token,
    )