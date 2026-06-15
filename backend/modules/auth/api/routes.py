from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.session import get_db
from modules.auth.application.schemas import LoginRequest, TokenResponse
from modules.auth.application.usecases import LoginUseCase
from modules.user.infrastructure.repositories import SQLAlchemyUserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    repo = SQLAlchemyUserRepository(db)

    token = LoginUseCase(repo).execute(
        form_data.username,
        form_data.password,
    )

    return TokenResponse(
        access_token=token,
    )