# Standard Library
from typing import List

# Third Party Stuff
from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="language")
    phrases: Mapped[List["Phrase"]] = relationship(back_populates="language")



class Direction(Base):
    __tablename__ = "directions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    phrase_code: Mapped[str] = mapped_column(String(50), nullable=False)

    users: Mapped[List["User"]] = relationship(back_populates="direction")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=True)
    direction_id: Mapped[int] = mapped_column(
        ForeignKey("directions.id"), nullable=True
    )

    direction: Mapped[Direction] = relationship(back_populates="users")
    language: Mapped[Language] = relationship(back_populates="users")


# Модель фраз бота на разных языках
class Phrase(Base):
    __tablename__ = "phrases"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    phrase_code: Mapped[str] = mapped_column(String(50), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=True)

    language: Mapped[Language] = relationship(back_populates="phrases")

    UniqueConstraint(language_id, phrase_code, name="unique_phrase")