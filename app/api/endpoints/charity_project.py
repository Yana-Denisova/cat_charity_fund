from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate, CharityProjectDB
from app.api.validators import check_name_duplicate, check_charity_project_exists, check_if_project_closed, check_sum, check_if_invested
from app.donation_service.donation_processor import donation_processor
router = APIRouter()


@router.post(
    '/',
    response_model_exclude_none=True,
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await donation_processor(session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model_exclude_none=True,
    response_model=list[CharityProjectDB],
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    #dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id, session
    )
    await check_if_project_closed(project)
    if obj_in.full_amount is not None:
        await check_sum(project=project, new_full_amount=obj_in.full_amount)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    updated_project = await charity_project_crud.update(
        project, obj_in, session
    )
    return updated_project


@router.delete(
    '/{project_id}',
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_charity_project_exists(
        project_id, session
    )
    await check_if_invested(project)
    project_deleted = await charity_project_crud.remove(project, session)
    return project_deleted
