from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class NewSungjukModel(BaseModel):

    name = Column(String, index=True)
    kor = Column(Integer)
    eng = Column(Integer)
    mat = Column(Integer)



class SungjukModel(NewSungjukModel):

    sjno: int
    regdate: datetime