from pydantic import BaseModel




class User(BaseModel):
    email: str
    full_name: str
    password: str
    id: int = 0

class GetUser(BaseModel):
    email: str
    full_name: str
    id: int
class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    def get_all(self):
        return self.users

    def get_by_email(self, email):
        for user in self.users:
            if email == user.email:
                return user
        return None

    def get_by_name(self, name):
        for user in self.users:
            if name == user.full_name:
                return user
        return None

    def get_by_id(self, id):
        for user in self.users:
            if id == user.id:
                return user
        return None

    def save(self, user):
        user.id = self.get_next_id()
        self.users.append(user)
        return user

    def get_next_id(self):
        return len(self.users) + 1

