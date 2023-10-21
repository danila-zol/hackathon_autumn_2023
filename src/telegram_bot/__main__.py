import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from auth import Login
from auth import Authenticator
import asyncio

dp = Dispatcher()
auth = Authenticator()

@dp.message(CommandStart())
async def begin(message: Message) -> None:
    await message.answer(
        f"Добро пожаловать, {hbold(message.from_user.full_name)}!\n" +
        "Я — Эфирный Курьер." + 
        "Я помогу вам быстро и удобно составить накладную, отследить заказ или составить жалобу." +
        "Для начала авторизуйтесь."
    )

@dp.message(Command("login"))
async def login(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите номер контракта"
    )
    await state.set_state(Login.get_cotract_id)

@dp.message(
    Login.get_cotract_id
)
async def got_contract_id(message: Message, state: FSMContext):
    message.answer("Проверяю номер контракта")
    if not auth.check_contract_id(message.text.lower()):
        message.answer(
            "Номер контракта не найден"
        )
        return
    
    await message.answer(
        "Номер контракта успешно найден"
    )
    await message.answer(
        "Введите пароль"
    )
    await state.set_state(Login.get_password)

@dp.message(
    Login.get_password
)
async def got_password(message: Message, state: FSMContext):
    if not auth.check_password(message.text.lower()):
        message.answer(
            "Неверный пароль"
        )
        return
    
    message.answer(
        "Авторизация успешна"
    )
    
    state.set_state(Login.logged_in)

async def main():
    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]

    bot = Bot(api_key)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
