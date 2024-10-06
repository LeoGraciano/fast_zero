from sqlalchemy import select

from fast_zero.models import User


def email_existis(email, session):
    result = session.scalar(select(User).where(User.email == email))
    return True if result else False
