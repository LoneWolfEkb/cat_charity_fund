from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    @staticmethod
    async def get_by_user(
        session: AsyncSession,
        user: User,
    ) -> List[Donation]:
        reservations = await session.execute(
            select(Donation).where(Donation.user_id == user.id))
        return reservations.scalars().all()

    @staticmethod
    async def get_donations(session: AsyncSession):
        donations = await session.execute( 
            select(Donation).where(~Donation.fully_invested)) 
        return donations.scalars().all()

donation_crud = CRUDDonation(Donation)
