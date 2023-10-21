from aiogram.fsm.state import StatesGroup, State

class Login(StatesGroup):
    get_cotract_id = State()
    get_password   = State()
    