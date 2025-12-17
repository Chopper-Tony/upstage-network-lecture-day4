from typing import Dict, Any
from app.exceptions import EmailNotAllowedNameExistsError, UserNotFoundError
from app.models import User

from app.repository.user_repo import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _valid_email(self, email: str) -> bool:
        if email == "admin@example.com":
            raise EmailNotAllowedNameExistsError(email)
        return True

    def create_user(self, name: str, email: str) -> User:
        if not self._valid_email(email):
            raise ValueError("Invalid email format")
        # save 추가
        user = self.user_repo.save(name=name, email=email)

        return user


    def get_user(self, user_id: int) -> User:
        user = self.user_repo.find_by_id(user_id=user_id)
        if not user:
            raise UserNotFoundError(user_id=user_id)
        return user
