from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud, donation_crud
#from app.models import CharityProject, Donation


async def investing(session: AsyncSession):
    donations = donation_crud.get_donations(session=session)
    projects = charity_project_crud.get_projects(session=session)
    donation_n = 0
    project_n = 0
    while donation_n < len(donations) and project_n < len(projects):
        free_for_investing = min(
            donations[donation_n].full_amount -
            donations[donation_n].invested_amount,
            projects[project_n].full_amount -
            projects[project_n].invested_amount)
        donations[donation_n].invested_amount += free_for_investing
        projects[project_n].invested_amount += free_for_investing
        if (donations[donation_n].full_amount ==
                donations[donation_n].invested_amount):
            donations[donation_n].fully_invested = True
            donations[donation_n].close_date = datetime.now()
            donation_n += 1
        if (projects[project_n].full_amount ==
                projects[project_n].invested_amount):
            projects[project_n].fully_invested = True
            projects[project_n].close_date = datetime.now()
            project_n += 1
    session.add_all(donations + projects)
    await session.commit()
