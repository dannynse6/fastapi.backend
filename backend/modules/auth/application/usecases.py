from fastapi import HTTPException

from core.security import (
    verify_password,
    create_access_token,
)


class LoginUseCase:

    def __init__(self, user_repo):
        self.user_repo = user_repo

    def execute(self, email, password):

        user = self.user_repo.get_by_email(email)

        if not user:
            raise HTTPException(401)

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(401)

        return create_access_token(user)
