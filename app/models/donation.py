from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from .general import General


class Donation(General, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
