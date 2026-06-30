from fastapi import APIRouter
from sqlalchemy.orm import Session
from modules.auth.application.schemas import LoginRequest, TokenResponse
from modules.auth.application.usecases import LoginUseCase
from modules.user.infrastructure.repositories import SQLAlchemyUserRepository
from core.dependencies import DBSession, LoginForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: LoginForm,
    db: DBSession,
):
    repo = SQLAlchemyUserRepository(db)

    token = LoginUseCase(repo).execute(
        form_data.username,
        form_data.password,
    )

    return TokenResponse(
        access_token=token,
    )