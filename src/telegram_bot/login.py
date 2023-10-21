from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import Dispatcher

from __main__ import dp, usage_commands, auth


class Login(StatesGroup):
    getting_contract_id = State()
    getting_password    = State()
    logged_in           = State()


@dp.message(CommandStart())
async def begin(message: Message, state: FSMContext) -> None:
    await message.answer(
    f"Добро пожаловать, {message.from_user.full_name}! Я — Эфирный Курьер. " + 
    "Я помогу вам быстро и удобно составить накладную, отследить заказ или составить жалобу.\n" +
    "Для начала следует авторизоваться"
   )
    await message.answer(
        "Введите пожалуйста номер вашего договора"
    )
    await state.set_state(Login.getting_contract_id)


@dp.message(Login.getting_contract_id)
async def got_contract_id(message: Message, state: FSMContext):
    await message.answer("Проверяю номер контракта")

    if not auth.check_contract_id(message.text.lower()):
        await message.answer("Такой номер договора не найден")
        return

    await message.answer("Успех! Теперь введите пароль")
    await state.set_state(Login.getting_password)


@dp.message(Login.getting_password)
async def food_size_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer("Проверяю пароль")

    if not auth.check_password(message.text.lower()):
        await message.answer("Пароль неверный")
        return

    await message.answer(
        "Авторизация успешна! Теперь вы можете:\n" +
        "\n".join(["— "+command+" : "+description for command, description in usage_commands.items()])
    )
    await state.set_state(Login.logged_in)