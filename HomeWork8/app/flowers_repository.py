from pydantic import BaseModel



class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0

class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = []


    def get_all(self)-> list[Flower]:
        return self.flowers

    def get_by_name(self, name):
        for flower in self.flowers:
            if name == flower.name:
                return flower
        return None

    def get_by_id(self, id):
        for flower in self.flowers:
            if id == flower.id:
                return flower
        return None

    def save(self, flower):
        flower.id = self.get_next_id()
        self.flowers.append(flower)
        return flower

    def get_next_id(self):
        return len(self.flowers) + 1


