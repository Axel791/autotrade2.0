from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateOrder(StatesGroup):
    description = State()
    purchase_count = State()
    sale_count = State()
    payment_type = State()
