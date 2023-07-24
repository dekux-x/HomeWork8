from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
from attrs import define
from pydantic import BaseModel

from .database import Base


class Flower(Base):
    __tablename__ = "flowers"

    name = Column(String, index = True)
    count = Column(Integer)
    cost = Column(Integer)
    id = Column( Integer, primary_key=True, index=True)

class FlowerCreate(BaseModel):
    name: str
    count: int
    cost: int

class FlowersRepository:
    def get_by_id(self, db: Session, flower_id: int):
        return db.query(Flower).filter(Flower.id == flower_id).first()


    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Flower).offset(skip).limit(limit).all()


    def save(self, db: Session, flower: FlowerCreate):
        db_flower = Flower(name=flower.name, count=flower.count,cost=flower.cost)

        db.add(db_flower)
        db.commit()
        db.refresh(db_flower)
        return db_flower


    def get_by_name(self, db: Session, name: str):
        return db.query(Flower).filter(Flower.name == name).first()




