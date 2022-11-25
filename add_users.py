import asyncio

from app.core.containers import Container
from app.models.telegram_user import TelegramUser

from dependency_injector.wiring import Provide, inject

USERS = {
    "user_1": {
        "first_name": "Дмитрий",
        "last_name": "Осипенко",
        "patronymic": "Владимирович",
        "phone_number": "+79661976776",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    },
    "user_2": {
        "first_name": "Юрий",
        "last_name": "Осипенко",
        "patronymic": "Владимирович",
        "phone_number": "+79163955090",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    },
    "user_3": {
        "first_name": "Алексей",
        "last_name": "Будков",
        "patronymic": "Викторович",
        "phone_number": "+79773102070",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    },
    "user_4": {
        "first_name": "Нурия",
        "last_name": "Хуснутдинова",
        "patronymic": "Яхияевна",
        "phone_number": "+79776102079",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.financier,
    },
    "user_5": {
        "first_name": "Татьяна",
        "last_name": "Жуйкова",
        "patronymic": "Михайловна",
        "phone_number": "+79164262903",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.financier,
    },
    "user_6": {
        "first_name": "Роман",
        "last_name": "Нырков",
        "patronymic": "Валерьевич",
        "phone_number": "+79683946040",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_7": {
        "first_name": "Роман",
        "last_name": "Нырков",
        "patronymic": "Валерьевич",
        "phone_number": "+79263927108",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_8": {
        "first_name": "Денис",
        "last_name": "Веретенов",
        "patronymic": "Андреевич",
        "phone_number": "+79260347807",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_9": {
        "first_name": "Александр",
        "last_name": "Машнин",
        "patronymic": "Алексеевич",
        "phone_number": "+79252999008",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_10": {
        "first_name": "Сергей",
        "last_name": "Иванов",
        "patronymic": "Юрьевич",
        "phone_number": "+79214533549",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_11": {
        "first_name": "Николай",
        "last_name": "Будаев",
        "patronymic": "Иванович",
        "phone_number": "+79091567474",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.manager,
    },
    "user_12": {
        "first_name": "Александр",
        "last_name": "Юрко",
        "patronymic": "Николаевич",
        "phone_number": "+79267556641",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_13": {
        "first_name": "Александр",
        "last_name": "Юрко",
        "patronymic": "Николаевич",
        "phone_number": "+79013843345",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_14": {
        "first_name": "Сергей",
        "last_name": "Зенченков",
        "patronymic": "Петрович",
        "phone_number": "+79854145119",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_15": {
        "first_name": "Сергей",
        "last_name": "Зенченков",
        "patronymic": "Петрович",
        "phone_number": "+79779415116",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_16": {
        "first_name": "Денис",
        "last_name": "Бажин",
        "patronymic": "Юрьевич",
        "phone_number": "+79250379938",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_17": {
        "first_name": "Николай",
        "last_name": "Бровко",
        "patronymic": "Алексеевич",
        "phone_number": "+79031921924",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_18": {
        "first_name": "Дмитрий",
        "last_name": "Виноградов",
        "patronymic": "Валентинович",
        "phone_number": "+79778137377",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_19": {
        "first_name": "Дмитрий",
        "last_name": "Виноградов",
        "patronymic": "Валентинович",
        "phone_number": "+79652813737",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.driver,
    },
    "user_20": {
        "first_name": "Тимофей",
        "last_name": "Казаков",
        "patronymic": "Андреевич",
        "phone_number": "+79172300481",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    },
    "user_21": {
        "first_name": "Полина",
        "last_name": "Тест",
        "patronymic": "Тест",
        "phone_number": "+79775311140",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    },
    "user_22": {
        "first_name": "Тест пользователь",
        "last_name": "Тест пользователь",
        "patronymic": "Тест пользоваитель",
        "phone_number": "+79159882039",
        "working_status": TelegramUser.WorkingStatus.worked,
        "permission_status": TelegramUser.PermissionStatus.super_user,
    }
}


@inject
async def add_users(telegram_user_service=Provide[Container.service_telegram_user]):
    telegram_user_service = telegram_user_service.provider()
    await telegram_user_service.create_users(users=value)


if __name__ == "__main__":
    for value in USERS.values():
        asyncio.run(add_users(users=value))
