from models import User
from models.users import add_user, find_user, get_user_by_id


def test_user_creation_and_attributes():
    user = User(1, "Алексей", "a@example.com")
    assert user.id == 1
    assert user.name == "Алексей"
    assert user.email == "a@example.com"


def test_user_str():
    assert str(User(1, "Алексей", "a@example.com")) == (
        "Алексей <a@example.com>")


def test_user_from_data():
    user = User.from_data(
        {"id": 2, "name": "Мария", "email": "m@example.com"})
    assert isinstance(user, User)
    assert user.id == 2
    assert user.to_dict()["email"] == "m@example.com"


def test_add_find_get_user():
    users = []
    add_user(users, "Алексей", "a@example.com")
    add_user(users, "Мария", "m@example.com")
    assert [u.id for u in users] == [1, 2]
    assert find_user(users, "мар")[0].name == "Мария"
    assert get_user_by_id(users, 2) is users[1]
    assert get_user_by_id(users, 9) is None
