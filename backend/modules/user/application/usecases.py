from fastapi import HTTPException, status
from core.security import verify_password, create_access_token
from modules.user.domain.repositories import UserRepository


class LoginUseCase:

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def execute(self, email: str, password: str) -> str:
        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is inactive",
            )

        return create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        )