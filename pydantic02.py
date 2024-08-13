from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from uuid import uuid4, UUID

app = FastAPI()

# Pydantic 모델 정의
class User(BaseModel):
    userid: UUID
    passwd: str
    name: str
    email: EmailStr
    regdate: datetime

# In-memory 데이터베이스 역할을 할 리스트
users_db = []

# Create - 새로운 회원 추가
@app.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

# Read - 모든 회원 조회
@app.get("/users/", response_model=List[User])
def read_users():
    return users_db

# Read - 특정 회원 조회
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: UUID):
    for user in users_db:
        if user.userid == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Update - 특정 회원 정보 수정
@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: UUID, updated_user: User):
    for index, user in enumerate(users_db):
        if user.userid == user_id:
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

# Delete - 특정 회원 삭제
@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: UUID):
    for index, user in enumerate(users_db):
        if user.userid == user_id:
            deleted_user = users_db.pop(index)
            return deleted_user
    raise HTTPException(status_code=404, detail="User not found")

# 예시 회원 추가
@app.on_event("startup")
def startup_event():
    example_user = User(
        userid=uuid4(),
        passwd="password123",
        name="John Doe",
        email="johndoe@example.com",
        regdate=datetime.now()
    )
    users_db.append(example_user)

