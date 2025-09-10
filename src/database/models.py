from datetime import date

from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    surname: Mapped[str] = mapped_column(String, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, unique=True)
    birthday: Mapped[date] = mapped_column(Date)
    additional_info: Mapped[str] = mapped_column(String)
