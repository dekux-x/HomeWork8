from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from attrs import define
from pydantic import BaseModel
from .database import Base



class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flower_id = Column(Integer, ForeignKey("flowers.id"))

class PurchaseCreate():
    user_id: int
    flower_id: int

    def __init__(self, user_id: int, flower_id: int):
        self.user_id = user_id
        self.flower_id = flower_id

class PurchasesRepository:
    def get_by_id(self, db: Session, user_id: int):
        return db.query(Purchase).filter(Purchase.user_id == user_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Purchase).offset(skip).limit(limit).all()

    def save(self, db: Session, purchase: PurchaseCreate):
        db_purchase = Purchase(user_id = purchase.user_id, flower_id = purchase.flower_id)

        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)
        return db_purchase

    def get_all_by_id(self, db: Session, user_id: int):
        return db.query(Purchase).filter(Purchase.user_id == user_id).all()

