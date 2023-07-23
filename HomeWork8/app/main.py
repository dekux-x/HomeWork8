import json

from fastapi import Cookie, FastAPI, Form, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from .flowers_repository import Flower, FlowersRepository
from .purchases_repository import Purchase, PurchasesRepository
from .users_repository import User, UsersRepository, GetUser

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


flowers_repository = FlowersRepository()
purchases_repository = PurchasesRepository()
users_repository = UsersRepository()



@app.post("/signup/")
def post_sign_ap(
        user: User
        ):
    if users_repository.get_by_email( user.email):
        return "There is already exist such user"
    users_repository.save(user)
    return "OK"

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
        password: str = Form()
):
    user = users_repository.get_by_name(username)
    if user.password == password:
            token = encode_jwt(user.id)
            return {"access_token": token, "type": "bearer"}
    return Response("There is no such user", status_code=404)

@app.get("/profile", response_model= GetUser)
def profile(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    user = users_repository.get_by_id(user_id)
    if user:
        return user
    return Response("There is problems with cookie", status_code=404)

@app.get("/flowers")
def get_flowers( ):
    flowers = flowers_repository.get_all()
    return flowers

@app.post("/flowers")
def post_flowers(flower: Flower):
    flowers_repository.save(flower)
    return flowers_repository.get_by_name(flower.name).id



@app.get("/cart/items")
def cart_items( cart: str = Cookie(default="[]")):
    cart_json = json.loads(cart)
    flowers = []
    for i in cart_json:
        flowers.append(flowers_repository.get_by_id(i["id"]))
    total = 0
    flowers_to_show = []
    for i in flowers:
        total += int(i.cost)
        flowers_to_show.append({"id": i.id, "name": i.name, "cost": i.cost})
    return {"total": total, "flowers": flowers_to_show}



@app.post("/cart/items")
def post_cart_items(response: Response, flower_id: int, cart = Cookie(default="[]")):
    flower = flowers_repository.get_by_id(flower_id)
    cart_json = json.loads(cart)
    if flower:
        data = {"id": flower.id}
        cart_json.append(data)
        new_cart = json.dumps(cart_json)
        response = Response("Ok")
        response.set_cookie("cart", new_cart)
    return response

@app.get("/purchased")
def get_purchase( token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    purchases = purchases_repository.get_all_by_id(user_id)
    flowers = []
    for purchase in purchases:
        flower = flowers_repository.get_by_id(purchase.flower_id)
        if flower:
            flowers.append({"id": flower.id, "name": flower.name})
    return flowers

@app.post("/purchased")
def post_purchase(cart: str = Cookie(default="[]"), token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt(token)
    cart_json = json.loads(cart)
    for i in cart_json:
        purchase = Purchase(user_id, i["id"])
        purchases_repository.save(purchase)
    return "Ok"