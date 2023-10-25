from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)

    users: Mapped[List["User"]] = relationship("User", backref="language")


class Direction(Base):
    __tablename__ = "directions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phrase_code: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship("User", backref="direction")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    direction_id: Mapped[int] = mapped_column(ForeignKey("directions.id"), nullable=False)

    direction: Mapped[Direction] = relationship("Direction", backref="users")
    language: Mapped[Language] = relationship("Language", backref="users")


# Модель фраз бота на разных языках
class Phrase(Base):
    __tablename__ = "phrases"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    phrase_code: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=True)

    language: Mapped[Language] = relationship("Language", backref="phrases")
