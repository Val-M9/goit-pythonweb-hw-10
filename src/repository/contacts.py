from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, extract
from datetime import date, timedelta


from src.database.models import Contact
from src.schemas.schemas import ContactModel, ContactUpdate


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self, skip: int, limit: int, query: str | None = None
    ) -> list[Contact]:
        stmt = select(Contact).offset(skip).limit(limit)

        if query:
            search = f"%{query}%"
            stmt = stmt.where(
                or_(
                    Contact.name.ilike(search),
                    Contact.surname.ilike(search),
                    Contact.email.ilike(search),
                )
            )

        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()  # pyright: ignore[reportReturnType]

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(stmt)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact | None:
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return await self.get_contact_by_id(contact.id)

    async def update_contact(
        self, contact_id: int, body: ContactUpdate
    ) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)

        if contact:
            for field, value in body.model_dump(exclude_unset=True).items():
                setattr(contact, field, value)

            await self.db.commit()
            await self.db.refresh(contact)

        return contact

    async def delete_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_contacts_with_upcoming_birthdays(self, days: int) -> list[Contact]:

        today = date.today()
        end_date = today + timedelta(days=days)
        
        current_month = today.month
        current_day = today.day
        end_month = end_date.month
        end_day = end_date.day
        
        # If same year
        if today.year == end_date.year:
            stmt = select(Contact).where(
                or_(
                    # Same month: day between today and end_day
                    and_(
                        extract('month', Contact.birthday) == current_month,
                        extract('day', Contact.birthday) >= current_day,
                        extract('day', Contact.birthday) <= end_day if current_month == end_month else 31
                    ),
                    # Different months between today and end month
                    and_(
                        extract('month', Contact.birthday) > current_month,
                        extract('month', Contact.birthday) < end_month
                    ) if current_month != end_month else False,
                    # End month: day <= end_day
                    and_(
                        extract('month', Contact.birthday) == end_month,
                        extract('day', Contact.birthday) <= end_day
                    ) if current_month != end_month else False
                )
            )
        else:
            # Case when year boundary crossing
            stmt = select(Contact).where(
                or_(
                    # Rest of current year: from today to december 31
                    and_(
                        extract('month', Contact.birthday) == current_month,
                        extract('day', Contact.birthday) >= current_day
                    ),
                    # Months after current month in current year
                    extract('month', Contact.birthday) > current_month,
                    # Beginning of next year: january 1 to end_date
                    and_(
                        extract('month', Contact.birthday) <= end_month,
                        extract('day', Contact.birthday) <= end_day
                    )
                )
            )
        
        stmt = stmt.order_by(
            extract('month', Contact.birthday),
            extract('day', Contact.birthday)
        )
        
        contacts = await self.db.execute(stmt)
        return contacts.scalars().all()  # pyright: ignore[reportReturnType]
