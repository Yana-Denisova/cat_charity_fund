from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud


def close_obj(obj) -> None:
    setattr(obj, 'invested_amount', obj.full_amount)
    setattr(obj, 'fully_invested', True)
    setattr(obj, 'close_date', datetime.now())


async def donation_processor(
    session: AsyncSession
):
    projects_for_donation = await charity_project_crud.get_project_by_investments(session)
    for project in projects_for_donation:
        if project:
            while project.invested_amount != project.full_amount:
                donation = await donation_crud.get_donation_by_investments(session)
                if donation:
                    money_to_get = project.full_amount - project.invested_amount
                    remainder = donation.full_amount - donation.invested_amount
                    if money_to_get > remainder:
                        updated_invested = project.invested_amount + remainder
                        close_obj(donation)
                        setattr(project, 'invested_amount', updated_invested)
                    elif money_to_get == remainder:
                        close_obj(donation)
                        close_obj(project)
                    elif money_to_get < remainder:
                        updated_invested = donation.invested_amount + money_to_get
                        setattr(donation, 'invested_amount', updated_invested)
                        close_obj(project)
                    session.add(donation)
                else:
                    break
            session.add(project)
    await session.commit()
