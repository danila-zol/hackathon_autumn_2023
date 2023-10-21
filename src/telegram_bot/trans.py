import pickle

USER_TRANS_PATH = "./data/user_trans.pkl"

class Transmission:

    def __init__(
        self, 
        transmission_id: int,
        delivery_type: str = None, 
        positions: int = None, 
        embed: str = None, 
        measures: dict = None,         # weight included
        cost: tuple = None,
        address: tuple = None,
        payment: str = None,
        status: str = None):
        self.transmission_id = transmission_id
        self.delivery_type = delivery_type
        self.size = positions
        self.embeded = embed
        self.measures = measures
        self.cost = cost
        self.address = address
        self.payment = payment
        self.status = None


class TransChecker:

    def __init__(self):
        with open(USER_TRANS_PATH, "rb") as F:
            self.user_trans = pickle.load(F)

    def list_transmissions(self, user: str):
        if self.user_trans.get(user, -1) == -1:
            return False
        answer = [f"{self.user_trans[user][_].transmission_id}\n" for _ in self.user_trans[user]]
        return *answer

    def get_transmission_id(self, transmission: "Transmission"):
        return transmission.transmission_id

    def get_transmission_status(self, transmission: "Transmission"):
        if transmission.status is None:
            return False
        return f"Статус отправления: {self.status}"

            
# trans1 = Transmission(
#     transmission_id=1, 
#     delivery_type="Дверь—Дверь", 
#     size=4, 
#     embeded="Коробка с коробкой внутри.", 
#     measures={"length": 10, "width": 20, "height": 5, "weight": 0.5},
#     cost=1000,
#     address="ПМЗ: г. Ростов-на-Дону, ул. Мечникова д.149",
#     payment="отправителем по договору")
            
# trans2 = Transmission(
#     transmission_id=1, 
#     delivery_type="Дверь—Склад", 
#     size=1, 
#     embeded="Душа", 
#     measures={"length": 1, "width": 2, "height": 5, "weight": 0.01},
#     cost=1_000_000,
#     address="Врата Ада",
#     payment="оплата получателем")
            
# trans3 = Transmission(
#     transmission_id=1, 
#     delivery_type="Склад-Склад", 
#     size=7, 
#     embeded="Ящик с брикетами киселя", 
#     measures={"length": 15, "width": 30, "height": 8, "weight": 5},
#     cost=1000,
#     address="ПМЗ: г. Ростов-на-Дону, ул. Мечникова д.149",
#     payment="отправителем по договору")

# user_trans = {"123": [trans1, trans2], "456": [trans3]}

# with open("./data/user_trans.pkl", "ab") as F:
#     pickle.dump(trans1, F)