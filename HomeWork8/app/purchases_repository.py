from attrs import define


@define
class Purchase:
    user_id: int = 0
    flower_id: int = 0


class PurchasesRepository:
    purchases: list[Purchase]

    def __init__(self):
        self.purchases = []

    def get_all(self):
        return self.purchases

    def get_all_by_id(self, user_id):
        user_purchases = []
        for purchase in self.purchases:
            if purchase.user_id == user_id:
                user_purchases.append(purchase)
        return user_purchases

    def get_by_id(self, id):
        for purchase in self.purchases:
            if id == purchase.user_id:
                return purchase
        return None

    def save(self, purchase):
        self.purchases.append(purchase)
        return purchase
