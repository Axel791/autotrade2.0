import logging

from aiogram.utils import executor
from aiogram import Dispatcher

from loader import dp
from app.core.containers import Container

from app.handlers import (
    start,
    base_handler,
    create_order,
    report,
    driver,
    manager,
    views_orders
)
import add_users
import add_user

from app import middlewares

start.register_start_handler(dp)
create_order.register_create_order_handler(dp)
base_handler.register_base_handler(dp)
report.register_report_handler(dp)
driver.register_driver_handler(dp)
manager.register_manager_handlers(dp)
views_orders.register_views_orders_handlers(dp)


def on_startup(dispatcher: Dispatcher):
    middlewares.setup(dp=dispatcher)


if __name__ == "__main__":
    logging.basicConfig(
        format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
        level=logging.INFO,
        # level=logging.DEBUG,
    )
    container = Container()
    db = container.db()
    db.create_database()
    container.wire(modules=[start, create_order, report, driver, manager, views_orders, add_users, add_user])
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup(dispatcher=dp))
