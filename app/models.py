from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Mountain(Base):
    __tablename__ = "mountains"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    external_id: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    elevation_m: Mapped[int | None] = mapped_column(Integer, nullable=True)

    reviews: Mapped[list["Review"]] = relationship(back_populates="mountain", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    mountain_id: Mapped[int] = mapped_column(ForeignKey("mountains.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review_text: Mapped[str] = mapped_column(Text, nullable=False)

    mountain: Mapped[Mountain] = relationship(back_populates="reviews")
