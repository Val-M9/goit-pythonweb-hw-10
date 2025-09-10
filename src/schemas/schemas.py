from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import Optional


class ContactModel(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=25)
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class ContactResponse(ContactModel):
    id: int


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None


class BirthdaysResponse(BaseModel):
    message: str
    contacts: list[ContactResponse] = []
