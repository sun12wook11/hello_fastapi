from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.settings import config

engine = create_engine(config.sqlite_url, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_startup():
    pass

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    mno = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    regdate = Column(DateTime(timezone=True), default=datetime.utcnow)
