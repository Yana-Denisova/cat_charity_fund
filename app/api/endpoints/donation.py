from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import GetUserDonations, DonationBase, DonationsDB
from app.services.donation_processor import donation_processor

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationsDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров"""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[GetUserDonations],
    response_model_exclude_none=True
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Только для текущего пользователя"""
    my_donations = await donation_crud.get_by_user(user, session)
    return my_donations


@router.post(
    '/',
    response_model=GetUserDonations,
    response_model_exclude_none=True
)
async def create_new_donation(
    donation: DonationBase,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    new_donation = await donation_crud.create(obj_in=donation, session=session, user=user)
    await donation_processor(session)
    await session.refresh(new_donation)
    return new_donation
