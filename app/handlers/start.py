from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from dependency_injector.wiring import Provide, inject

from app.services.telegram_user import TelegramUserService
from app.services.validators import ValidateInformationService
from app.core.containers import Container
from app.utils.states.start_handler import StartState
from app.utils.keyboards.start import (
    superuser_keyboard,
    manager_keyboards,
    financier_and_accounting_keyboards,
    driver_keyboards
)


@inject
async def get_phone_number(message: types.Message):
    await message.answer("Отправьте номер телефона для авторизации: ")
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
        await message.answer(correct_phone_number)

    else:
        tg_user_dict = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
        }

        message_out = await telegram_user_service.registration_user(
            obj_in=tg_user_dict,
            phone_number=correct_phone_number
        )

        if message_out:
            await message.answer("Вы успешно авторизовались в системе!\n\n"
                                 f"Добро пожаловать, {message.from_user.first_name}\n"
                                 f"Перед вами меню:", reply_markup=superuser_keyboard)
            await state.finish()
        else:
            await message.answer("Такого номера нет в базе данных! Проверьте корректность его написания.")


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(get_phone_number, commands=["start"])
    dp.register_message_handler(start_command, state=StartState.phone_number)