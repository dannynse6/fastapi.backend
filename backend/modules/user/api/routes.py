from fastapi import APIRouter
from database.session import get_db
from core.dependencies import get_current_user, require_roles
from core.dependencies import CurrentUser, DBSession, AdminUser
from ..application.schemas import CreateUserRequest, UserResponse
from ..infrastructure.repositories import SQLAlchemyUserRepository
from ..application.usecases import CreateUserUseCase

router = APIRouter(
	prefix="/users",
	tags=["Users"],
)


@router.get("/me")
def me(current_user: CurrentUser):
	return current_user


@router.get("")
def list_users(current_user: AdminUser):
	return {
		"message": "Admin only"
	}


@router.post("", response_model=UserResponse)
def create_user(
		request: CreateUserRequest,
		db: DBSession,
):
	repo = SQLAlchemyUserRepository(db)
	user = CreateUserUseCase(repo).execute(
		email=str(request.email),
		password=request.password,
		role=request.role,
	)

	return user
