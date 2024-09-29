from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    data = {"email": "test@example.com", "password": "password123"}
    user = User(**data)

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == data.get("email")))

    assert result.email == data.get("email")
