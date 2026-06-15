from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from core.dependencies import get_current_user, require_roles
from ..application.schemas import CreateUserRequest, UserResponse
from ..infrastructure.repositories import SQLAlchemyUserRepository
from ..application.usecases import CreateUserUseCase

router = APIRouter(
	prefix="/users",
	tags=["Users"],
)


@router.get("/me")
def me(current_user=Depends(get_current_user)):
	return current_user


@router.get("")
def list_users(current_user=Depends(require_roles("ADMIN"))):
	return {
		"message": "Admin only"
	}


@router.post("", response_model=UserResponse)
def create_user(
		request: CreateUserRequest,
		db: Session = Depends(get_db),
):
	repo = SQLAlchemyUserRepository(db)
	user = CreateUserUseCase(repo).execute(
		email=request.email,
		password=request.password,
		role=request.role,
	)

	return user
