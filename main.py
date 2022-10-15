from aiogram.utils import executor
from aiogram_dialog import Dialog, DialogRegistry

from loader import dp
from app.core.containers import Container

from app.db.base import Base
from app.db.session import engine

from app.models.order import Order
from app.models.telegram_user import TelegramUser
from app.models.images import Images
from app.models.report import Report

from app.handlers import start
from app.handlers import create_order

# dialog = Dialog()
# registry.register(dialog)

start.register_start_handler(dp)
create_order.register_create_handler(dp)


def on_startup():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__, start, create_order])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
