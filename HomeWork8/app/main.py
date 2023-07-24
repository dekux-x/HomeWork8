import json

from fastapi import Cookie, FastAPI, Form, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt

from .flowers_repository import Flower, FlowersRepository, FlowerCreate
from .purchases_repository import PurchaseCreate, PurchasesRepository
from .users_repository import User, UsersRepository, GetUser, UserCreate
from .database import Base, engine, SessionLocal


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup/")
def post_sign_ap(
        user: UserCreate,
        db: Session = Depends(get_db)
        ):
    db_user = users_repository.get_by_email(db, user.email)
    if  db_user:
        raise HTTPException( status_code= 404, detail="User already exist")
    users_repository.save(db, user)
    return db_user

def encode_jwt(user_id: str):
    body = {"user_id": user_id}
    token = jwt.encode(body, "saidshabekov", "HS256")
    return token

def decode_jwt(token: str):
    body = jwt.decode(token, "saidshabekov", "HS256")
    return body["user_id"]

@app.post("/login")
def post_login(
        username: str = Form(),
        password: str = Form(),
        db: Session = Depends(get_db)
):
    user = users_repository.get_by_name(db, username)
    if user.password == password:
            token = encode_jwt(user.id)
            return {"access_token": token, "type": "bearer"}
    raise HTTPException(status_code=404, detail="There is no such user")

@app.get("/profile", response_model= GetUser)
def profile(token: str = Depends(oauth2_scheme),
            db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(db, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="There is no such user")

@app.get("/flowers")
def get_flowers(db: Session = Depends(get_db)):
    flowers = flowers_repository.get_all(db)
    return flowers

@app.post("/flowers")
def post_flowers(flower: FlowerCreate, db: Session = Depends(get_db)):
    flowers_repository.save(db, flower)
    return flowers_repository.get_by_name(db, flower.name).id



@app.get("/cart/items")
def cart_items( cart: str = Cookie(default="[]"),
                db: Session = Depends(get_db)):
    cart_json = json.loads(cart)
    flowers = []
    for i in cart_json:
        flowers.append(flowers_repository.get_by_id(db, i["id"]))
    total = 0
    flowers_to_show = []
    for i in flowers:
        total += int(i.cost)
        flowers_to_show.append({"id": i.id, "name": i.name, "cost": i.cost})
    return {"total": total, "flowers": flowers_to_show}



@app.post("/cart/items")
def post_cart_items(response: Response, flower_id: int, cart = Cookie(default="[]"), db: Session = Depends(get_db)):
    flower = flowers_repository.get_by_id(db, flower_id)
    cart_json = json.loads(cart)
    if flower:
        data = {"id": flower.id}
        cart_json.append(data)
        new_cart = json.dumps(cart_json)
        response = Response("Ok")
        response.set_cookie("cart", new_cart)
    return response

@app.get("/purchased")
def get_purchase(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    purchases = purchases_repository.get_all_by_id(db, user_id)
    flowers = []
    for purchase in purchases:
        flower = flowers_repository.get_by_id(db, purchase.flower_id)
        if flower:
            flowers.append({"id": flower.id, "name": flower.name})
    return flowers

@app.post("/purchased")
def post_purchase(cart: str = Cookie(default="[]"), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_jwt(token)
    cart_json = json.loads(cart)
    for i in cart_json:
        purchase = PurchaseCreate(user_id, i["id"])
        purchases_repository.save(db, purchase)
    return "Ok"