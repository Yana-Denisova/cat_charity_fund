from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import create_charity_project
from app.schemas.charity_project import CharityProjectCreate
from app.api.validators import check_name_duplicate

router = APIRouter()


@router.post('/charity_project/', response_model_exclude_none=True,)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    return new_project
