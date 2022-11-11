from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp
from app.core.containers import Container

from app.db.base import Base
from app.db.session import engine

from app.models.order import Order
from app.models.telegram_user import TelegramUser
from app.models.images import Images
from app.models.report import Report

from app.handlers import (
    start,
    base_handler,
    create_order,
    report,
    driver,
    manager,
    views_orders
)

from app.tests import create_user
from app import middlewares

start.register_start_handler(dp)
create_order.register_create_order_handler(dp)
base_handler.register_base_handler(dp)
report.register_report_handler(dp)
driver.register_driver_handler(dp)
manager.register_manager_handlers(dp)
views_orders.register_views_orders_handlers(dp)


def on_startup(dispatcher: Dispatcher):
    Base.metadata.create_all(bind=engine)
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[start, create_order, report, driver, manager, views_orders, create_user])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
