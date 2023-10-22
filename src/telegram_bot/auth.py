import pickle
import json
from aiogram.fsm.state import StatesGroup, State

USER_DICT_PATH = "./data/users_dict.pkl"
CONFIG_PATH = "./src/telegram_bot/config.json"

class Authenticator:

    users_dict = {}
    config = {}

    def __init__(self):
        with open(USER_DICT_PATH, "rb") as f:
            self.users_dict = pickle.load(f)
        
        with open(CONFIG_PATH) as f:
            self.config = json.load(f)

    def check_creds(contract_id, password):
        pass

    def add_creds(self, contract_id, password):

        self.users_dict[contract_id]["password"] = password

        with open(USER_DICT_PATH, "wb") as f:
            pickle.dump(self.users_dict, f)

    def del_creds(self, contract_id):

        if not self.users_dict.pop(contract_id, 0):
            return 0

        with open(USER_DICT_PATH, "wb") as f:
            pickle.dump(self.users_dict, f)
        
        return 1


    def is_admin(self, user_id):
        return True if user_id in self.config["admins"] else False
    
    def check_contract_id(self, contract_id):
        print(self.users_dict)
        return True if contract_id in self.users_dict.keys() else False
    
    def check_password(self, password):
        print(self.users_dict)
        return True if password in self.users_dict.values() else False


    