from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud


def close_obj(obj) -> None:
    setattr(obj, 'fully_invested', True)
    setattr(obj, 'close_date', datetime.now())


async def donation_processor(session: AsyncSession):
    projects_for_donation = await charity_project_crud.get_project_by_investments(session)
    for project in projects_for_donation:
        if project:
            donation = await donation_crud.get_donation_by_investments(session)
            if donation:
                money_to_get = project.full_amount - project.invested_amount
                remainder = donation.full_amount - donation.invested_amount
                free_for_investing = min(money_to_get, remainder)
                donation.invested_amount += free_for_investing
                project.invested_amount += free_for_investing
                if project.full_amount == project.invested_amount:
                    close_obj(project)
                if donation.full_amount == donation.invested_amount:
                    close_obj(donation)
                session.add(donation)
            session.add(project)
    await session.commit()
