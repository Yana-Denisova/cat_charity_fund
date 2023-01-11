from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import get_project_id_by_name, get_by_id
from app.models import CharityProject


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await get_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта не существует!'
        )
    return project


async def check_if_project_closed(
    project: CharityProject
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=422,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_sum(
    project: CharityProject,
    new_full_amount: int
) -> None:
    if project.invested_amount > new_full_amount:
        raise HTTPException(
            status_code=422,
            detail='Нельзя установить требуемую сумму меньше уже вложенной!'
        )


async def check_if_invested(
    project: CharityProject,
) -> None:
    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
