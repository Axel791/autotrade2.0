from app.repository.telegram_user import RepositoryTelegramUser


class TelegramUserService:

    def __init__(self, repository_telegram_user: RepositoryTelegramUser) -> None:
        self._repository_telegram_user = repository_telegram_user

    async def registration_user(self, phone_number: str, obj_in: dict) -> bool:
        user = self._repository_telegram_user.get(phone_number=phone_number)
        if user is None:
            return False

        elif user.user_id is None:
            self._repository_telegram_user.update(
                db_obj=user,
                obj_in=obj_in,
                commit=True
            )

        return True


