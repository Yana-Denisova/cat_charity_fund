from typing import Optional

from fastapi.encoders import jsonable_encoder

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.crud.base import CRUDBase


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id


charity_project_crud = CRUDCharityProject(CharityProject)


async def create_charity_project(
    new_project: CharityProjectCreate,
    session: AsyncSession,
) -> CharityProject:
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
    name: str,
    session: AsyncSession,
) -> Optional[int]:
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == name
        )
    )
    db_project_id = db_project_id.scalars().first()
    return db_project_id


async def get_all(
    session: AsyncSession,
) -> list[CharityProject]:
    db_project = await session.execute(select(CharityProject))
    return db_project.scalars().all()


async def get_by_id(
    project_id: int,
    session: AsyncSession,
) -> Optional[CharityProject]:
    db_project = await session.execute(
        select(CharityProject).where(
            CharityProject.id == project_id
        )
    )
    return db_project.scalars().first()


async def update_charity_project(
        db_project: CharityProject,
        project_in: CharityProjectUpdate,
        session: AsyncSession,
) -> CharityProject:
    obj_data = jsonable_encoder(db_project)
    update_data = project_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_project, field, update_data[field])
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def delete_project(
        db_project: CharityProject,
        session: AsyncSession,
) -> CharityProject:
    await session.delete(db_project)
    await session.commit()
    return db_project
