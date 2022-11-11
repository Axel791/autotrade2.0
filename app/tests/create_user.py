import asyncio

from app.services.telegram_user import TelegramUserService
from app.core.containers import Container
from app.models.telegram_user import TelegramUser
from dependency_injector.wiring import Provide, inject


@inject
async def create_user(telegram_user_service: TelegramUserService = Provide[Container.service_telegram_user]):
    user_dict = {
        "first_name": "Дмитрий",
        "last_name": "Майоров",
        "patronymic": "Евгеньевич",
        "phone_number": "+79152564823",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver
    }
    telegram_user = telegram_user_service.provider()

    return await telegram_user.create_user(user_dict=user_dict)


if __name__ == "__main__":
    asyncio.run(create_user())
