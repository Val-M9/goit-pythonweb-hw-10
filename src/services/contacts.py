from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.schemas import ContactModel, ContactUpdate


class ContactService:
    def __init__(self, db: AsyncSession):
        self.contact_repository = ContactRepository(db)

    async def get_contacts(self, skip: int, limit: int, query: str | None = None):
        return await self.contact_repository.get_contacts(skip, limit, query)

    async def get_contact_by_id(self, contact_id: int):
        return await self.contact_repository.get_contact_by_id(contact_id)

    async def create_contact(self, body: ContactModel):
        return await self.contact_repository.create_contact(body)

    async def update_contact(self, contact_id: int, body: ContactUpdate):
        return await self.contact_repository.update_contact(contact_id, body)

    async def delete_contact(self, contact_id: int):
        return await self.contact_repository.delete_contact(contact_id)

    async def get_contacts_with_upcoming_birthdays(self, days: int):
        return await self.contact_repository.get_contacts_with_upcoming_birthdays(
            days
        )
