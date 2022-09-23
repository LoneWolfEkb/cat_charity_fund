from sqlalchemy import Column, ForeignKey, Integer, Text

from .charity_base import CharityBase


class Donation(CharityBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
