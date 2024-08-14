# 회원정보를 이용한 SQL CRUD
# mno, userid, passwd, name, email, regdate

from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime

# 데이터베이스 설정 (python.db로 변경)
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'

    mno = Column(Integer, primary_key=True, index=True)
    userid = Column(String, unique=True, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    regdate = Column(DateTime(timezone=True), default=datetime.utcnow)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic 모델 정의
class MemberModel(BaseModel):
    mno: Optional[int] = None
    userid: str
    passwd: str
    name: str
    email: EmailStr
    regdate: Optional[datetime] = None

    class Config:
        from_attributes = True

app = FastAPI()

@app.get("/")
def index():
    return "Member management with SQLAlchemy and FastAPI!"

# 회원 등록
@app.post("/members/", response_model=MemberModel)
def create_member(member: MemberModel, db: Session = Depends(get_db)):
    db_member = Member(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# 전체 회원 조회
@app.get("/members/", response_model=List[MemberModel])
def read_members(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 특정 회원 조회
@app.get("/members/{mno}", response_model=Optional[MemberModel])
def read_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

# 회원 정보 수정
@app.put("/members/{mno}", response_model=Optional[MemberModel])
def update_member(mno: int, member: MemberModel, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.mno == mno).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    for key, value in member.dict(exclude_unset=True).items():
        setattr(db_member, key, value)

    db.commit()
    db.refresh(db_member)
    return db_member

# 회원 삭제
@app.delete("/members/{mno}", response_model=Optional[MemberModel])
def delete_member(mno: int, db: Session = Depends(get_db)):
    db_member = db.query(Member).filter(Member.mno == mno).first()
    if db_member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(db_member)
    db.commit()
    return db_member

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)
