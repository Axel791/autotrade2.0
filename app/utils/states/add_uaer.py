from aiogram.dispatcher.filters.state import State, StatesGroup


class User(StatesGroup):
    name = State()
    last_name = State()
    phone_number = State()
    permission_status = State()
