from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from login import Login
from __main__ import dp

class Complain(StatesGroup):
    getting_transport_id  = State()
    getting_complain_type = State()

class DeliveryTooLong(StatesGroup):
    pass

class DamagedItem(StatesGroup):
    pass

class LostItem(StatesGroup):
    pass

class DamagedPackaging(StatesGroup):
    pass

class MiscIssue(StatesGroup):
    pass

@dp.message(
    Command("/file_complain"),
    Login.logged_in
)
async def complain(msg: Message, state: FSMContext):
    msg.answer("По какому заказу вы бы хотели сделать жалобу?")
    state.set_state(Complain.getting_transport_id)