
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import select

sqlite_url = 'sqlite:///app/clouds2024.db'
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Zipcode(Base):

    __tablename__ = 'zipcode'

    zipcode = Column(String, index=True)
    sido = Column(String)
    gugun = Column(String)
    dong = Column(String)
    ri = Column(String)
    bunji = Column(String)
    seq = Column(String, primary_key=True)

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def index():
    return "Member management with jinja2!"

@app.get("/zipcode/{dong}")
def zipcode(dong: str):
    result = ''

    # sessionmaker 없이 디비 객체 직접 생성
    with Session(engine) as sess:
        stmt = select(Zipcode).where(Zipcode.dong.like(f'{dong}'))
        rows = sess.execute(stmt)

        for row in rows:
            result += f'{row.zipcode} {row.sido} {row.gugun} {row.dong}'

    return f'{result}'


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)
