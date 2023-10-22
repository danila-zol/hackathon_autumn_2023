from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Command, Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram import F
from login import Login
from __main__ import dp, auth

class Complain(StatesGroup):
    getting_transport_id  = State()
    weather_delivered = State()
    getting_complaint_type = State()


class DeliveryTooLong(StatesGroup):
    when_delivered    = State()


class DamagedItem(StatesGroup):
    what_damage = State()

class LostItem(StatesGroup):
    when_lost = State()


class DamagedPackaging(StatesGroup):
    what_damage = State


class MiscIssue(StatesGroup):
    describing = State()


complain_types_keys = [
    [
        [KeyboardButton(text="Нарушение сроков доставки")],
        [KeyboardButton(text="Порча вложение")]
    ],
    [
        [KeyboardButton(text="Утеря вложения")],
        [KeyboardButton(text="Повреждение упаковки")]
    ],
    [[KeyboardButton(text="Другое")]]
]

complain_types_kb = ReplyKeyboardMarkup(
    keyboard=complain_types_keys,
    resize_keyboard=True,
    input_field_placeholder="Выбирете тип жалобы"
)

@dp.message(
    Command("/file_complain"),
    Login.logged_in
)
async def complain(msg: Message, state: FSMContext):
    await msg.answer("По какому заказу вы бы хотели сделать жалобу?")
    state.set_state(Complain.getting_transport_id)


@dp.message(
    Complain.getting_transport_id
)
async def got_transport_id(msg: Message, state: FSMContext):
    found = False
    for e in auth.user_config.items():
        if msg.text.split()[1] in e[1]["transmissions"].keys():
            found = True
            state.update_data(contract_id=e[0])
            break
    
    # if not found:
    #     msg.answer("Такое отправление не найдено")
    #     state.set_state(Login.logged_in)
    #     return
    
    transmission_id = msg.text.split()[1]
    state.update_data(bad_transmission=transmission_id)
    await msg.answer("Какой тип вашей проблемы?", reply_markup=complain_types_kb)
    yes_no_kb = ReplyKeyboardMarkup(
        keyboard=["Да", "Нет"],
        resize_keyboard=True
        input_field_placeholder="Была ли посылка доставлена"
    )
    state.set_state(Complain.weather_delivered)


@dp.message(
        Complain.weather_delivered,
        F.text.lower() == "да"
)
async def delivered(msg: Message, state: FSMContext):
    state.update_data(delivered=True)


@dp.message(
        Complain.weather_delivered,
        F.text.lower() == "нет"
)
async def delivered(msg: Message, state: FSMContext):
    state.update_data(delivered=False)


@dp.message(
    Complain.getting_complain_type,
    F.text == "Нарушение сроков доставки"
)
async def got_complaint_type(msg: Message, state: FSMContext):
    data = state.get_data()
    msg.answer("Грустно")


@dp.message(
    Complain.getting_complain_type,
    F.text == "Порча вложение"
)
async def got_complaint_type(msg: Message, state: FSMContext):
    msg.answer("Грустно")

@dp.message(
    Complain.getting_complain_type,
    F.text == "Утеря вложения"
)
async def got_complaint_type(msg: Message, state: FSMContext):
    msg.answer("Грустно")

@dp.message(
    Complain.getting_complain_type,
    F.text == "Повреждение упаковки"
)
async def got_complaint_type(msg: Message, state: FSMContext):
    msg.answer("Грустно")

@dp.message(
    Complain.getting_complaint_type,
    F.text == "Другое"
)
async def got_complaint_type(msg: Message, state: FSMContext):
    msg.answer("Грустно")