from datetime import datetime 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import CharityProject
from app.crud.donation import donation_crud
from app.crud.charity_project import charity_project_crud


async def donation_processor(
    session: AsyncSession
):
    project_for_donation = await charity_project_crud.get_project_by_investments(session)
    if project_for_donation:
        while project_for_donation.invested_amount != project_for_donation.full_amount:
            donation = await donation_crud.get_donation_by_investments(session)
            if donation:
                money_to_get = project_for_donation.full_amount - project_for_donation.invested_amount
                print(f'надо на проект еще {money_to_get}')
                remainder = donation.full_amount - donation.invested_amount
                print(f'можно задонатить {remainder}')
                if money_to_get > remainder:
                    #we_have = money_to_get - remainder
                    #print(f'we have {we_have}')
                    updated_invested = project_for_donation.invested_amount + remainder
                    print(f'updated_invested {updated_invested}')
                    setattr(project_for_donation, 'invested_amount', updated_invested)
                    setattr(donation, 'invested_amount', donation.full_amount)
                    setattr(donation, 'fully_invested', True)
                    setattr(donation, 'close_date', datetime.now())
                elif money_to_get == remainder:
                    setattr(project_for_donation, 'fully_invested', True)
                    setattr(project_for_donation, 'invested_amount', project_for_donation.full_amount)
                    setattr(project_for_donation, 'close_date', datetime.now())
                    setattr(donation, 'invested_amount', donation.full_amount)
                    setattr(donation, 'fully_invested', True)
                    setattr(donation, 'close_date', datetime.now())
                elif money_to_get < remainder:
                    we_have = remainder - money_to_get
                    updated_invested = donation.invested_amount + money_to_get
                    setattr(donation, 'invested_amount', updated_invested)
                    setattr(project_for_donation, 'fully_invested', True)
                    setattr(project_for_donation, 'invested_amount', project_for_donation.full_amount)
                    setattr(project_for_donation, 'close_date', datetime.now())
                session.add(donation)
            else:
                break
        session.add(project_for_donation)
    await session.commit()
