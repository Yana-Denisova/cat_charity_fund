from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_by_user(
        self,
        user: User,
        session: AsyncSession,
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()

    async def get_donation_by_investments(
        self,
        session: AsyncSession
    ) -> Optional[Donation]:
        available_donation = await session.execute(
            select(Donation).where(
                Donation.fully_invested == False).order_by(Donation.create_date)
            )
        return available_donation.scalars().first()


donation_crud = CRUDDonation(Donation)
