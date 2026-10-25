"""Класс User и функции работы с коллекцией пользователей."""
from typing import Any, List, Optional

from .base import Entity


class User(Entity):
    """Пользователь системы."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        """Создать пользователя."""
        super().__init__(user_id)
        self.name = name
        self.email = email

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря данных JSON."""
        return cls(data["id"], data["name"], data["email"])

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать пользователя в данные для JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        return f"{self.name} <{self.email}>"


def add_user(users: List[User], name: str, email: str) -> None:
    """Создать пользователя и добавить его в коллекцию."""
    new_id = max((u.id for u in users), default=0) + 1
    users.append(User(new_id, name, email))


def get_user_by_id(users: List[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None


def find_user(users: List[User], query: str) -> List[User]:
    """Найти пользователей по подстроке имени или e-mail."""
    query = query.lower()
    return [
        u for u in users
        if query in u.name.lower() or query in u.email.lower()
    ]


def show_users(users: List[User]) -> None:
    """Вывести список пользователей."""
    for user in users:
        print(f"{user.id}. {user}")
