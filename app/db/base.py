from typing import Any, ClassVar

from sqlalchemy.orm import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.
    It automatically generates the __tablename__.
    """

    id: Any
    __name__: str
    __tablename__: ClassVar[str]

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
