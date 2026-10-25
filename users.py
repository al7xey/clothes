"""Пользователи системы."""
from typing import Optional


def add_user(users: dict[int, dict], name: str, email: str) -> int:
    """Добавить пользователя и вернуть его идентификатор."""
    new_id = max(users, default=0) + 1
    users[new_id] = {"id": new_id, "name": name, "email": email}
    return new_id


def get_user(users: dict[int, dict], user_id: int) -> Optional[dict]:
    """Найти пользователя по идентификатору."""
    return users.get(user_id)


def find_user(users: dict[int, dict], query: str) -> list[dict]:
    """Найти пользователей по подстроке имени или e-mail."""
    query = query.lower()
    return [
        user for user in users.values()
        if query in user["name"].lower() or query in user["email"].lower()
    ]
