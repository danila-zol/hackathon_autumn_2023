import pickle

USER_DICT_PATH = "./data/user_dict.pkl"

# class Transmission:

#     def __init__(
#         self, 
#         transmission_id: int,
#         delivery_type: str = None, 
#         positions: int = None, 
#         embed: str = None, 
#         measures: dict = None,         # weight included
#         cost: tuple = None,
#         address: tuple = None,
#         payment: str = None,
#         status: str = None):
#         self.transmission_id = transmission_id
#         self.delivery_type = delivery_type
#         self.size = positions
#         self.embeded = embed
#         self.measures = measures
#         self.cost = cost
#         self.address = address
#         self.payment = payment
#         self.status = None


class TransChecker:

    def __init__(self):
        with open(USER_DICT_PATH, "rb") as f:
            self.user_dict = pickle.load(f)

    def list_transmissions(self, contract_id: str):
        if self.user_dict[contract_id].get("transmissions", -1) == -1:
            return False
        answer = [f"{self.user_dict[contract_id]['transmissions'][_]}\n" for _ in self.user_trans[contract_id]['transmissions']]
        return answer

    def get_transmission_status(self, transmission):
        if self.user_dict[transmission]["status"] is None:
            return False
        return f"Статус отправления: {self.user_dict[transmission]['status']}"

    def create_bill(self, bill_dict: dict):
        if self.user_dict.get("bills", -1) == -1:
            self.user_dict.update({"bills": []})
        temp = self.user_dict["bills"]
        temp.append(bill_dict)
        self.user_dict.update({"bills": temp})
        with open(USER_DICT_PATH, "wb") as f:
            pickle.dump(self.user_dict, f)
            
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