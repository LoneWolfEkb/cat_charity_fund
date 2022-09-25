from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_id_by_name(
            name: str, session: AsyncSession) -> Union[int, None]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == name))
        return db_project_id.scalars().first()

    @staticmethod
    async def get_projects_to_elaborate(session: AsyncSession):
        projects = await session.execute(
            select(CharityProject).where(CharityProject.fully_invested == False).order_by(CharityProject.create_date))
        return projects.scalars().all()


project_crud = CRUDCharityProject(CharityProject)
