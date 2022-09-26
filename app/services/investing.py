from datetime import datetime
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import CharityProjectDB
from app.schemas.donation import DonationAdminDB


async def fully_invested(obj: Union[CharityProjectDB,
                                    DonationAdminDB]) -> None:
    obj.fully_invested = True
    obj.invested_amount = obj.full_amount
    obj.close_date = datetime.now()


async def investing(donation: DonationAdminDB,
                    project: CharityProjectDB) -> bool:
    if donation.fully_invested or project.fully_invested:
        return True

    donation_to_use = donation.full_amount - (donation.invested_amount or 0)
    project_required = project.full_amount - (project.invested_amount or 0)
    if project_required < donation_to_use:
        donation.invested_amount += project_required
        await fully_invested(project)
    elif project_required > donation_to_use:
        project.invested_amount += donation_to_use
        await fully_invested(donation)
    else:
        await fully_invested(donation)
        await fully_invested(project)


async def donation_investing(
    session: AsyncSession,
    donation: DonationAdminDB) -> List[CharityProjectDB]:
    projects = await project_crud.get_projects_to_elaborate(session=session)
    projects_elaborated = []
    for project in projects:
        projects_elaborated.append(project)
        if await investing(donation=donation, project=project):
            break
    return projects_elaborated


async def project_investing(
    session: AsyncSession,
    project: CharityProjectDB) -> List[DonationAdminDB]:
    donations = await donation_crud.get_donations_to_elaborate(session=session)
    donations_elaborated = []
    for donation in donations:
        donations_elaborated.append(donation)
        if await investing(donation=donation, project=project):
            break
    return donations_elaborated
