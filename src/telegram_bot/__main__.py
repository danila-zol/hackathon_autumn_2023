import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from auth import Authenticator, Login
from trans import Transmission, TransChecker
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


dp = Dispatcher()
auth = Authenticator()
tc = TransChecker()

class Usage(StatesGroup):
    stand_by           = State()        # Стэйт, на который юзер переходит, когда отменяет команду. Также не позволяет запускать комадны в других командах
    ask_transmissions  = State()
    track_transmission = State()
    create_bill        = State()
    report_problem     = State()


class Login(StatesGroup):
    getting_contract_id = State()
    getting_password    = State()
    logged_in           = State()


usage_commands = {
    "`/list`": "Вывести список отправлений",
    "`/track`": "Узнать статус заказа",
    "`/bill`": "Создать новую накладную",
    "`/report`": "Зарегестрировать претензию",
    "`/help`": "Получить сообщение со справкой",
}

@dp.message(CommandStart())
async def begin(message: Message, state: FSMContext) -> None:
    await message.answer(
        f"""
        Добро пожаловать, {hbold(message.from_user.full_name)}! 
        Я — Эфирный Курьер.
        Я помогу вам быстро и удобно составить накладную, отследить заказ или составить жалобу.
        Для следует авторизоваться. Введите пожалуйста номер вашего договора
        """
   )
    await state.set_state(Login.getting_contract_id)


@dp.message(Login.getting_contract_id)
async def got_contract_id(message: Message, state: FSMContext):
    await message.answer("Проверяю номер контракта")

    if not auth.check_contract_id(message.text.lower()):
        await message.answer("Такой номер договора не найден")
        return

    await message.answer("Теперь введите пароль")
    await state.set_state(Login.getting_password)


@dp.message(Login.getting_password)
async def food_size_chosen_incorrectly(message: Message, state: FSMContext):
    await message.answer("Проверяю пароль")

    if not auth.check_password(message.text.lower()):
        await message.answer("Пароль неверный")
        return

    await message.answer(
        "Авторизация успешна. Теперь вы можете:\n" +
        "\n".join(["— "+command+" : "+description for command, description in usage_commands.items()])
    )
    await state.set_state(Login.logged_in)


@dp.message(Login.logged_in, Command("list"))
async def give_transmissions(message: Message, state: FSMContext):
    await message.answer("Получение списка отправлений. Пожалуйста, подождите")
    if not tc.list_transmissions():
        message.answer("По вашему номеру договора ничего не найдено.")
    message.send(tc.list_transmissions())             # Как определить юзера?

@dp.message(Login.logged_in, Command("help"))
async def give_help(message: Message, state: FSMContext):
    await message.answer("Справка по использованию бота:\n" +
        "\n".join(["— "+command+" : "+description for command, description in usage_commands.items()])
    )

@dp.message(Login.logged_in, Command("track"))
async def track_transmission(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите номер отправления, которое хотите отследить\n"+
        "`/cancel` для отмены."
    )
    state.set_state(Usage.track_transmission)

@dp.message(Login.logged_in, Usage.track_transmission)
async def got_transmission_id(message: Message, state: FSMContext):
    await message.answer("Получение информации по отправлению. Пожалуйста, подождите")
    if not tc.get_transmission_status(message.text.lower()):
        message.answer("Заказ не найден. Проверьте написание номера и попробуйте ещё раз")
    message.answer(tc.get_transmission_id(message.text.lower()))
    state.set_state(Usage.stand_by)

@dp.message(Login.logged_in, Usage.stand_by, Command("bill"))
async def new_bill(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите")

# @dp.message(F.text)
# async def send_state(message : Message, state : FSMContext):
#     current_state = await state.get_state()
#     print(f"Current state: {current_state}")
#     message.answer(f"Current state: {current_state}")


async def main():
    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]

    bot = Bot(api_key)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
