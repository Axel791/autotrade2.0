from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram_dialog import DialogManager, Window, Dialog, StartMode, DialogRegistry
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format

from app.utils.states.create_oder_state import CreateOrder
from loader import bot, dp

registry = DialogRegistry(dp)


async def start_creating_order(message: types.Message):
    await message.answer("Введите описание к заказу:")
    await CreateOrder.next()


async def get_bot_id(message: types.Message):
    bot_id = await bot.get_me()
    await message.answer(bot_id)


async def check_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


class MySG(StatesGroup):
    main = State()
    not_main = State()


async def get_data(**kwargs):
    return {
        "name": "Тимофей"
    }

main_window = Window(
    Const("Hello!"),
    Button(Const("Button"), id="nothing"),
    state=MySG.main
)

with_name_btn = Window(
    Format("Hello, {name}!"),
    Button(Const("test_btn"), id="nothing"),
    state=MySG.not_main,
    getter=get_data,
)

dialog = Dialog(main_window, with_name_btn)
registry.register(dialog)


async def check_aiogram_dialog(mes: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


async def get_with_name(mes: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.not_main, mode=StartMode.RESET_STACK)


def register_create_handler(dp: Dispatcher):
    dp.register_message_handler(start_creating_order, lambda message: message.text == 'Сформировать заказ📝')
    dp.register_message_handler(check_description, state=CreateOrder.description)

    dp.register_message_handler(check_aiogram_dialog, commands=["dialog"])
    dp.register_message_handler(get_with_name, commands=["start_2"])