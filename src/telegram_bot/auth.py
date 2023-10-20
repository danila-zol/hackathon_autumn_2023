import pickle
import json

USER_DICT_PATH = "./data/user_dict.pickle"
CONFIG_PATH = "./src/telegram_bot/config.json"

class Authenticator:

    user_dict = {}
    config = {}

    def __init__(self):
        with open(USER_DICT_PATH) as f:
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

    
