from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import get_project_id_by_name


async def check_name_duplicate(
        name: str,
        session: AsyncSession,
) -> None:
    room_id = await get_project_id_by_name(name, session)
    if room_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Проект с таким именем уже существует!',
        )
