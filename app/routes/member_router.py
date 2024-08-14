from typing import Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from app.models.member import Member
from sqlalchemy02 import MemberModel, NewMemberModel

member_router = APIRouter()

# @member_router.get("/")
# def index():
#     return 'Hello, member router!!'

@member_router.get('/list', response_model=list[MemberModel])
def list(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members


# 회원 등록
# @app.post("/members/", response_model=NewMemberModel)
@member_router.post("/add", response_model=NewMemberModel)
def create_member(member: NewMemberModel, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


# 특정 회원 조회
@member_router.get("/view/{mno}", response_model=Optional[MemberModel])
def read_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member


# 회원 정보 수정
@member_router.put("/update/{mno}", response_model=Optional[MemberModel])
def update_member(mno: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.mno == mno).first()
    db.commit()
    db.refresh(db_member)
    return db_member

# 회원 삭제
@member_router.delete("/delete/{mno}", response_model=Optional[MemberModel])
def delete_member(mno: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.mno == mno).first()
    db.delete(db_member)
    db.commit()
    return db_member