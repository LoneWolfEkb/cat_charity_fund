from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationAdminDB


async def fully_invested(obj: Union[CharityProjectDB, DonationAdminDB]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investing(session: AsyncSession, donation: DonationAdminDB, project: CharityProjectDB) -> None:
    donation_to_use = donation.full_amount - (donation.invested_amount or 0)
    project_required = project.full_amount - (project.invested_amount or 0)
    if project_required < donation_to_use:
        await fully_invested(project)
        donation.invested_amount += project_required
    elif project_required > donation_to_use:
        project.invested_amount += donation_to_use
        await fully_invested(donation)
    else:
        await fully_invested(donation)
        await fully_invested(project)
    session.add(project)
    session.add(donation)


async def donation_investing(session: AsyncSession, donation: DonationAdminDB) -> None:
    projects = await project_crud.get_projects_to_elaborate(session=session)
    for project in projects:
        await investing(session=session, donation=donation, project=project)
    await session.commit()
    await session.refresh(donation)


async def project_investing(session: AsyncSession, project: CharityProjectDB) -> None:
    donations = await donation_crud.get_donations_to_elaborate(session=session)
    for donation in donations:
        await investing(session=session, donation=donation, project=project)
    await session.commit()
    await session.refresh(project)
