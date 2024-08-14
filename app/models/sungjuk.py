from pip._internal.utils import datetime
from sqlalchemy import Integer, Column, String, DateTime
from datetime import datetime
from app.models.base import Base


class SungjukModel(Base):
    __tablename__ = 'sungjuk'
    sjno= Column (Integer, primary_key=True, autoincrement=True, index=True)
    name= Column (String, index=True)
    kor= Column (Integer)
    eng= Column (Integer)
    mat= Column (Integer)
    regdate = Column (DateTime(timezone=True), default=datetime.now)