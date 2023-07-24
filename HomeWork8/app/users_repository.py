from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from attrs import define
from pydantic import BaseModel

from .database import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String, unique=True)
    id = Column(Integer, primary_key=True, index=True)


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str


class GetUser(BaseModel):
    email: str
    full_name: str
    id: int

class UsersRepository:
    def get_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def save(self, db: Session, user: UserCreate):
        db_user = User(email=user.email, password=user.password, full_name = user.full_name)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_by_name(self, db: Session, name: str):
        return db.query(User).filter(User.full_name == name).first()



