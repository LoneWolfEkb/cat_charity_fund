from typing import Optional

from pydantic import BaseSettings, EmailStr

TITLE = 'Кошачий благотворительный фонд'
DESCRIPTION = 'Сервис для поддержки котиков!'


class Settings(BaseSettings):
    app_title: str = TITLE
    app_description: str = DESCRIPTION
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
