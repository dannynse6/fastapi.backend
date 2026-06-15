from sqlalchemy.orm import Session

from .models import UserModel


class SQLAlchemyUserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str):
        return (
            self.db.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

    def get_by_id(self, user_id: int):
        return (
            self.db.query(UserModel)
            .filter(UserModel.id == user_id)
            .first()
        )

    def create(self, email: str, hashed_password: str, role: str):
        user = UserModel(
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_active=True,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user