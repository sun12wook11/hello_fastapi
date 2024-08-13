from fastapi import FastAPI
from pydantic import BaseModel
from typing_extensions import List


# pydantic
# 데이터 유효성 검사 및 직렬화/역직렬화 지원 도구
# docs.pydantic.dev
# pip install pydantic
class Sungjuk(BaseModel):
    name: str
    kor: int
    eng: int
    mat: int


# 성적 데이터 저장용 변수
sungjuk_db: List[Sungjuk] = []

app = FastAPI()


@app.get("/")
def index():
    return "Hello Pydantic!!"

# 성적데이터 조회
# response_model : 응답데이터 형식 지정
# 이를 통해 클라이언트는 서버가 어떤 종류의 데이터를 보내는지 알수있음
@app.get("/sj", response_model=List[Sungjuk])
def sj_readall():
    return sungjuk_db

@app.post("/sjadd", response_model=Sungjuk)
def sj_create(sj: Sungjuk):
    sj = Sungjuk()
    sungjuk_db.append(sj)
    return sj

# 성적데이터상세조회 이름으로 조회
@app.get('/sjone/{name}', response_model=Sungjuk)
def sjone(name: str):
    findone = None
    for sj in sungjuk_db:
      if sj.name == name:
            findone = sj
    return findone

#샘플 성적 데이터 추가 :
@app.get('/sjadd', response_model=Sungjuk)
def sj_create():00.
    sj = Sungjuk(name='혜교',kor=99, eng=98, mat=99)
    sungjuk_db.append(sj)

    sj = Sungjuk(name='지현',kor=44, eng=55, mat=66)
    sungjuk_db.append(sj)

    sj = Sungjuk(name='수지',kor=77, eng=88, mat=91)
    sungjuk_db.append(sj)
    return sj

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('pydantic01:app', reload=True)

@app.post("/sjadd", response_model=Sungjuk)
def sj_create(sj: Sungjuk):
    sj = Sungjuk()
    sungjuk_db.append(sj)
    return sj

@app.delete('/sj/', resource_model=Sungjuk)
def sjrmv(name: str):
    rmvone = Sungjuk(name='none',kor=00,eng=00,mat=00)
    for idx, sj in enumerate(sungjuk_db):
        if sj.name == name:
            rmvone = sungjuk_db.pop(idx)
    return rmvone

