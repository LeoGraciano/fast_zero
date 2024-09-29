from datetime import datetime
from uuid import uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


class BasicFieldsMixin:
    id: Mapped[str] = mapped_column(init=False, primary_key=True, default=str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(init=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        init=False,
        server_onupdate=func.now(),
        nullable=True,
    )


@table_registry.mapped_as_dataclass
class User(BasicFieldsMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
