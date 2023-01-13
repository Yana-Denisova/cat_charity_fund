from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import get_project_id_by_name, get_by_id
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
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


def check_if_project_closed(
    project: CharityProject
) -> None:
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


def check_sum(
    project: CharityProject,
    obj_in: CharityProjectUpdate,
) -> None:
    if (
        project.invested_amount > obj_in.full_amount
    ):
        raise HTTPException(
            status_code=400,
            detail="Нельзя установить сумму, ниже уже вложенной!"
        )


async def check_if_invested(
    project: CharityProject,
) -> None:
    if project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
