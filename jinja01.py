from fastapi import FastAPI, Request
from sqlalchemy import create_engine, Column, String, select
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


# jinja2Template
# 파이썬용 템플릿 엔진
# 다양한 웹 프레임워크에서 템플릿 렌더링을 위해 사용
# 템플릿(html)에 동적으로 데이터(디비, 조회, 객체)를 삽입해서
# 최종 결과물을 만드는 담당 역할
# jinja.palllet


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
templates = Jinja2Templates(directory='views/templates')  # Ensure this directory is correct


@app.get("/")
def index():
    return "Member management with jinja2!"


@app.get("/zipcode/{dong}")
def zipcode(dong: str):
    result = []
    with Session(engine) as sess:
        stmt = select(Zipcode).where(Zipcode.dong.like(f'{dong}%'))
        rows = sess.execute(stmt).all()
        for row in rows:
            result.append(f'{row.zipcode} {row.sido} {row.gugun} {row.dong}')
    # Send result to the template
    return templates.TemplateResponse('zipcode.html', {"zipcodes": result})


@app.get("/zipcode2/{dong}", response_class=HTMLResponse)
def zipcode2(dong: str, req: Request):
    # 짚코드 검색  result 결과 저장
    # with Session(engine) as sess:
    #     stmt = select(Zipcode).where(Zipcode.dong.like(f'{dong}%'))
    #     results = sess.execute(stmt).scalars().all() # v2


    with Session(engine) as sess:
        where = Zipcode.dong.like(f'{dong}%')
        result = sess.query(Zipcode).filter(where).all() # v1

       # 저장된 검색결과를 템플릿 엔진을 이용해서 html 결과문서를 만들기 위해
       # Pass results and request path to the template
    return templates.TemplateResponse('zipcode.html',
                {"zipcodes": result, 'path': req.url.path,'sayhello':'Hello, jinja2'})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('sqlalchemy02:app', reload=True)
