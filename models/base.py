"""Базовый класс сущностей предметной области."""
from typing import Any


class Entity:
    """Сущность с уникальным идентификатором.

    Все сущности проекта «являются» Entity: у каждой есть id и умение
    представить себя данными для JSON (полиморфизм to_dict()).
    """

    def __init__(self, entity_id: int) -> None:
        """Сохранить идентификатор сущности."""
        self._id = entity_id

    @property
    def id(self) -> int:
        """Идентификатор только для чтения (инкапсуляция)."""
        return self._id

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать сущность в данные для JSON."""
        raise NotImplementedError("Метод переопределяется в наследниках")
