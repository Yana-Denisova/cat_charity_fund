from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.donation  import donation_crud
from app.schemas.donation import GetUserDonations

router = APIRouter()

@router.get(
    '/',
    response_model_exclude_none=True,
    #dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров"""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/me',
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
