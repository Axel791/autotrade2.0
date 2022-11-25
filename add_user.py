import asyncio

from app.core.containers import Container
from app.models.telegram_user import TelegramUser

from dependency_injector.wiring import Provide, inject


USER = {
    "first_name": "Николай",
    "last_name": "Бровко",
    "patronymic": "Пусто",
    "phone_number": "+79251924630",
    "working_status": TelegramUser.WorkingStatus.worked,
    "permission_status": TelegramUser.PermissionStatus.driver,
}


@inject
async def add_user(user: dict, telegram_user_service=Provide[Container.service_telegram_user]):
    telegram_user_service = telegram_user_service.provider()
    await telegram_user_service.create_users(users=user)


if __name__ == "__main__":
    asyncio.run(add_user(user=USER))

