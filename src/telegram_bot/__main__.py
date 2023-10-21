import json
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from auth import Authenticator
from trans import Transmission, TransChecker
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

dp = Dispatcher()
auth = Authenticator()
tc = TransChecker()

import management
from login import Login

usage_commands = {
    "/list": "Вывести список отправлений",
    "/track": "Узнать статус заказа",
    "/bill": "Создать новую накладную",
    "/report": "Зарегестрировать претензию",
    "/help": "Получить сообщение со справкой",
}

class Usage(StatesGroup):
    stand_by               = State()        # Стэйт, на который юзер переходит, когда отменяет команду. Также не позволяет запускать комадны в других командах
    ask_transmissions      = State()
    track_transmission     = State()
    get_bill_items         = State()
    get_bill_mode          = State()
    get_item_positions     = State()
    get_embed_description  = State()
    got_all_desc           = State()
    get_place_measurements = State()
    get_embed_price        = State()
    get_address_type       = State()
    get_address            = State()
    get_payment            = State()
    report_problem         = State()

bill_form = {

}

@dp.message(Login.logged_in, Command("cancel"))
async def cancel_operation(message: Message, state: FSMContext):
    if not state == Usage.stand_by:
        message.answer("Отмена операции")
        state.set_state(Usage.stand_by)
        bill_form.clear()
        item_descriptions.clear()
        iterations = 1

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

@dp.message(Login.logged_in, Usage.stand_by, Command("track"))
async def track_transmission(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите номер отправления, которое хотите отследить\n"+
        "\n/cancel для отмены."
    )
    state.set_state(Usage.track_transmission)

@dp.message(Login.logged_in, Usage.track_transmission)
async def got_transmission_id(message: Message, state: FSMContext):
    await message.answer("Получение информации по отправлению. Пожалуйста, подождите")
    if not tc.get_transmission_status(message.text.lower()):
        message.answer("Заказ не найден. Проверьте номер и попробуйте ещё раз")
    message.answer(tc.get_transmission_id(message.text.lower()))
    state.set_state(Usage.stand_by)

@dp.message(Login.logged_in, Usage.stand_by, Command("bill"))
async def new_bill(message: Message, state: FSMContext):
    await message.answer(
        "Пожалуйста, введите количество позиций.\n" +
        "\n/cancel для отмены."
    )
    state.set_state(Usage.get_bill_items)

transmission_modes = ["дверь-дверь", "склад-склад", "склад-дверь", "дверь-склад"]
@dp.message(Login.logged_in, Usage.get_bill_items)
async def new_bill(message: Message, state: FSMContext):
    if not isinstance(message.text, int):
        message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    bill_form.update({"items": message.text})
    message.answer(
        "Пожалуйста, введите режим доставки.\n" +
        "\n".join(transmission_modes) +
        "\n\n/cancel для отмены."
    )
    state.set_state(Usage.get_bill_mode)

@dp.message(Login.logged_in, Usage.get_bill_mode)
async def got_bill_mode(message: Message, state: FSMContext):
    if message.text.lower not in transmission_modes:
        message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    bill_form.update({"mode": message.text.lower()})
    message.answer(
        "Пожалуйста, введите количество мест." +
        "\n/cancel для отмены."
    )
    state.set_state(Usage.get_embed_description)

@dp.message(Login.logged_in, Usage.get_embed_description)
async def got_bill_positions(message: Message, state: FSMContext):
    if not isinstance(message.text, int):
        message.answer("Некорректно введены данные. Пожалуйста, повторите попытку.")
        return
    bill_form.update({"positions": message.text})
    message.answer(
        "Пожалуйста, введите описание каждого товара по отдельности" +
        "\n\n/undo для сброса последней позиции" +
        "\n/retry чтобы начать сначала" +
        "\n/cancel для отмены."
    )
    state.set_state(Usage.get_bill_description)

item_descriptions = []
iterations = 1

@dp.message(Login.logged_in, Usage.get_embed_description, Command("undo"))
async def undo_description(message: Message, iterations: int = iterations):
    item_descriptions.pop()
    iterations -= 1
    message.answer(f"Описание позиции {iterations} удалено.")

@dp.message(Login.logged_in, Usage.get_embed_description, Command("retry"))
async def retry_descriptions(message: Message, state: FSMContext, iterations: int = iterations):
    iterations = 1
    item_descriptions.clear()
    message.answer("Описания всех позиций стёрты.")

@dp.message(
    Login.logged_in,
    Usage.get_embed_description
    )
async def got_one_description(message: Message, state: FSMContext, iterations: int = iterations):
    if iterations == bill_form["items"]:
        message.answer("Все позиции записаны.\n" +
            "\n".join([_ for _ in item_descriptions]) +
                        "\n\n/confirm для подтверждения" + 
                        "\n/undo для сброса последней позиции"+
                        "\n/retry чтобы начать сначала" +
                        "\n/cancel для отмены."
                        )   
        state.set_state(Usage.got_all_desc)
        return
    
    item_descriptions.append(message.text)
    message.answer(
        f"Описание позиции {iterations} записано."+
        "\n\n/undo для сброса последней позиции"+
        "\n/retry чтобы начать сначала" +
        "\n/cancel для отмены."
        )   
    iterations += 1 

@dp.message(Login.logged_in, Usage.got_all_desc)
async def ask_measurements(message: Message, state: FSMContext):
    message.answer("Пожалуйста, напишите измерения каждого места.")
    state.set_state(Usage.get_place_measurements)

# @dp.message(F.text)
# async def send_state(message : Message, state : FSMContext):
#     current_state = await state.get_state()
#     print(f"Current state: {current_state}")
#     await message.answer(f"Current state: {current_state}")


async def main():
    with open("src/telegram_bot/api_key.json") as f:
        api_key = json.load(f)["api_key"]

    bot = Bot(api_key)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
