from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.models.base import Base


class Member(Base):
    __tablename__ = 'members'

    mno = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime, default=datetime.now)