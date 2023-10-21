import pickle
import json
from aiogram.fsm.state import StatesGroup, State

USER_DICT_PATH = "./data/user_dict.pkl"
CONFIG_PATH = "./src/telegram_bot/config.json"

class Authenticator:

    user_dict = {}
    config = {}

    def __init__(self):
        with open(USER_DICT_PATH, "rb") as f:
            user_dict = pickle.load(f)
        
        with open(CONFIG_PATH) as f:
            config = json.load(f)

    def check_creds(contract_id, password):
        pass

    def add_creds(self, contract_id, password):

        self.user_dict[contract_id] = password

        with open(USER_DICT_PATH) as f:
            pickle.dump(self.user_dict, f)

    def is_admin(self, user_id):
        return True if user_id in self.config["admins"] else False
    
    def check_contract_id(self, contract_id):
        return True if contract_id in self.user_dict.keys() else False
    
    def check_password(self, password):
        return True if password in self.user_dict.values() else False



class Login(StatesGroup):
    get_cotract_id = State()
    get_password   = State()
    logged_in      = State()


    