import re

from phonenumbers import format_number, parse
from phonenumbers import PhoneNumberFormat
from phonenumbers.phonenumberutil import NumberParseException


class ValidateInformationService:

    @classmethod
    async def validate_phone_number(cls, phone_number: str) -> str:
        error_message = "Неправильный формат номера телефона," \
                        " проверьте правильность написания и отправьте боту снова:" \
                        f"Отправленный вами номер: {phone_number}"

        if not re.compile("^[0-9+().,-]+$").search(string=phone_number) is not None:
            return error_message

        try:
            number = parse(number=phone_number, region='RU')
            valid_number = format_number(number, PhoneNumberFormat.E164)

            if len(valid_number) < 12:
                return error_message

        except NumberParseException:
            return error_message

        return valid_number





