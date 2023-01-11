from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold

from dependency_injector.wiring import Provide, inject

from app.services.telegram_user import TelegramUserService
from app.services.validators import ValidateInformationService

from app.core.containers import Container
from app.utils.states.add_uaer import User

from app.utils.states.start_handler import StartState
from app.utils.keyboards.start import (
    superuser_keyboard,
    manager_keyboards,
    financier_and_accounting_keyboards,
    driver_keyboards,
    role
)
from app.models.telegram_user import TelegramUser


@inject
async def get_phone_number(message: types.Message):
    await message.answer("📱Отправьте номер телефона для авторизации: ")
    await StartState.phone_number.set()


@inject
async def start_command(
        message: types.Message,
        state: FSMContext,
        telegram_user_service: TelegramUserService = Provide[Container.service_telegram_user],
        validate_service: ValidateInformationService = Provide[Container.validate_service],
):
    phone = message.text
    correct_phone_number = await validate_service.validate_phone_number(phone_number=phone)

    if len(correct_phone_number) > 12:
        await message.answer(f"⛔️Не правильный номер телефона, проверьте его написанрие: {correct_phone_number}")

    else:
        tg_user_dict = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
        }
        print(correct_phone_number)
        message_out = await telegram_user_service.registration_user(
            obj_in=tg_user_dict,
            phone_number=correct_phone_number
        )

        if message_out:
            user_perm_status = await telegram_user_service.get_user_permission_status(user_id=message.from_user.id)
            if user_perm_status == TelegramUser.PermissionStatus.super_user:
                await message.answer(f"{hbold('Вы успешно авторизовались в системе✅')}\n\n"
                                     f"Добро пожаловать, {hbold(message.from_user.first_name)}!\n"
                                     f"Перед вами меню:", reply_markup=superuser_keyboard)
            elif user_perm_status == TelegramUser.PermissionStatus.driver:
                await message.answer(f"{hbold('Вы успешно авторизовались в системе✅')}\n\n"
                                     f"Добро пожаловать, {hbold(message.from_user.first_name)}!\n"
                                     f"Перед вами меню:", reply_markup=driver_keyboards)
            elif user_perm_status == TelegramUser.PermissionStatus.manager:
                await message.answer(f"{hbold('Вы успешно авторизовались в системе✅')}\n\n"
                                     f"Добро пожаловать, {hbold(message.from_user.first_name)}!\n"
                                     f"Перед вами меню:", reply_markup=manager_keyboards)
            elif user_perm_status == TelegramUser.PermissionStatus.financier:
                await message.answer(f"{hbold('Вы успешно авторизовались в системе✅')}\n\n"
                                     f"Добро пожаловать, {hbold(message.from_user.first_name)}!\n"
                                     f"Перед вами меню:", reply_markup=financier_and_accounting_keyboards)
            await state.finish()
        else:
            await message.answer("⛔️Такого номера нет в базе данных! Проверьте корректность его написания.")


@inject
async def users(
        message: types.Message,
        tg_user_service: TelegramUserService = Provide[Container.service_telegram_user]
):
    user_id = message.from_user.id
    if user_id == 688136452:
        users = await tg_user_service.list()
        for user in users:
            await message.answer(
                f"{user.id}\n"
                f"{user.first_name}\n"
                f"{user.last_name}\n"
                f"{user.user_id}\n"
                f"{user.username}\n"
                f"{user.permission_status}\n"

            )


async def add_user(message: types.Message):
    await message.answer("Напишите имя:")
    await User.name.set()


async def name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    await message.answer("Напишите фамилию: ")
    await User.last_name.set()


async def last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["last_name"] = message.text
    await message.answer("Напишите номер телефона через + на 7, пример(+79102231278): ")
    await User.phone_number.set()


async def phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number"] = message.text
    await message.answer("Выберите роль: ", reply_markup=role)
    await User.permission_status.set()


@inject
async def get_role(
        callback_query: types.CallbackQuery,
        state: FSMContext,
        telegram_user_service: TelegramUserService = Provide[Container.service_telegram_user],
):
    data_role = callback_query.data
    async with state.proxy() as data:
        name = data.get("name")
        last_name = data.get("last_name")
        phone_number = data.get("phone_number")
    if data_role == "manager":
        role = TelegramUser.PermissionStatus.manager
    elif data_role == "driver":
        role = TelegramUser.PermissionStatus.driver
    elif data_role == "fin":
        role = TelegramUser.PermissionStatus.financier
    else:
        role = TelegramUser.PermissionStatus.super_user
    obj_in = {
        "first_name": name,
        "last_name": last_name,
        "phone_number": phone_number,
        "permission_status": role
    }
    await telegram_user_service.create(obj_in=obj_in)
    await callback_query.message.answer("Создан!")
    await state.finish()


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(add_user, commands=["add_user"])
    dp.register_message_handler(name, state=User.name)
    dp.register_message_handler(last_name, state=User.last_name)
    dp.register_message_handler(phone_number, state=User.phone_number)
    dp.register_callback_query_handler(get_role, state=User.permission_status)
    dp.register_message_handler(get_phone_number, commands=["start"])
    dp.register_message_handler(start_command, state=StartState.phone_number)
    dp.register_message_handler(users, commands=["user"])
