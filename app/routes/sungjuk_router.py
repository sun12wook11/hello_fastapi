from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from sqlalchemy01 import SungjukModel, Sungjuk

sungjuk_router = APIRouter()

# @sungjuk_router.get("/")
# def index():
#     return "Hello, sungjuk router!!"

@sungjuk_router.get('/list', response_model=list[SungjukModel])
def read_sj(db: Session = Depends(get_db)):
    sungjuks = db.query(Sungjuk).all()
    return sungjuks



# 회원 등록
# @app.post("/members/", response_model=NewMemberModel)
@sungjuk_router.post("/add", response_model=SungjukModel)
def sjadd(sj: SungjukModel, db: Session = Depends(get_db)):
    sj = Sungjuk(**dict(sj)) # 클라이언트가 전송한 성적 데이터가
    # pydanmic으로 유효성 검사후
    # 데이터베이스에 저장할수 있도록
    # sqlalchemy 객체로 변함
    # py : Sungjuk(name=?, kor=?, eng=?, mat=?)
    # sa : Sungjuk(sj['name'], sj['kor'], sj['eng'], sj['mat'])
    db.add(sj)
    db.commit()
    db.refresh(sj)
    return sj


# 특정 회원 조회
@sungjuk_router.get("/view/{mno}", response_model=Optional[SungjukModel])
def readone_sj(sjno: int, db: Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sjno).first()
    return sungjuk


# 회원 정보 수정
@sungjuk_router.put("/update/{mno}", response_model=Optional[SungjukModel])
def update_sj(sj:SungjukModel, db: Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sj.sjno).first()
    if sungjuk:
        for key, val in sj.dict().items():
            setattr(sungjuk, key, val)
        db.commit()
        db.refresh(sungjuk)
    return sungjuk

# 회원 삭제
@sungjuk_router.delete("/delete/{mno}", response_model=Optional[SungjukModel])
def delete_sj(sjno: int, db: Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sjno).first()
    if sungjuk:
        db.delete(sungjuk)
        db.commit()
    return sungjuk