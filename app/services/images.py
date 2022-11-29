from loguru import logger

from loader import bot

from aiogram.utils.exceptions import BotBlocked
from aiogram.utils.markdown import hbold

from app.repository.images import RepositoryImages
from app.repository.telegram_user import RepositoryTelegramUser
from app.repository.order import RepositoryOrder

from app.utils.keyboards.form_inline_keyboard import FormInlineKeyboardService

from app.models.images import Images
from app.models.order import Order


class ImagesService:

    def __init__(
            self,
            repository_telegram_user: RepositoryTelegramUser,
            repository_images: RepositoryImages,
            repository_order: RepositoryOrder,

            keyboard_service: FormInlineKeyboardService
    ):
        self._repository_telegram_user = repository_telegram_user
        self._repository_images = repository_images
        self._repository_order = repository_order
        self._keyboard_service = keyboard_service

    async def create_images(
            self,
            image: str,
            image_description: str,
            order_id: int
    ) -> Images:

        order = self._repository_order.get(id=order_id)
        obj_in = {
            "order_id": order.id,
            "image": image,
            "image_description": image_description,
            "image_status": Images.ImageStatus.in_work,
            "user_id": None,
            "user": None,
            "order": order
        }
        image = self._repository_images.create(obj_in=obj_in)

        return image

    async def get_images_by_order(self, image_status, order_id) -> list:
        images = self._repository_images.list(
            order_id=order_id,
            image_status=image_status
        )

        return images

    async def update_images_status(
            self,
            image_id: str,
            user_id: str,
            image_status: Images.ImageStatus,
            image_status_past: Images.ImageStatus
    ):
        user = self._repository_telegram_user.get(user_id=user_id)

        obj_in = {
            "image_status": image_status,
            "user_id": user.id,
            "user": user
        }
        db_obj = self._repository_images.get(id=image_id)

        update_images = self._repository_images.update(
            obj_in=obj_in,
            db_obj=db_obj,
            commit=True
        )

        logger.info(f"{image_status}: image_status")
        logger.info(f"{image_status_past} image_status_past")

        db_obj_order = self._repository_order.get(id=db_obj.order_id)
        obj_in_order = {
            "order_status": Order.OrderStatusWork.partially_assembled
        }

        logger.info(update_images.order.user.user_id)
        images_assembled = self._repository_images.list(
                order_id=db_obj.order_id,
                image_status=Images.ImageStatus.assembled
        )

        image_delivered = self._repository_images.list(
            order_id=db_obj.order_id,
            image_status=Images.ImageStatus.delivered
        )

        image_in_work = self._repository_images.list(
            order_id=db_obj.order_id,
            image_status=Images.ImageStatus.in_work
        )

        logger.info(f"{image_delivered} : image_delivered")
        logger.info(f"{images_assembled} : images_assembled")
        logger.info(f"{image_in_work} : image_in_work")

        if not image_in_work:
            obj_in_order = {"order_status": Order.OrderStatusWork.assembled}
            logger.info("Зашли если ет вообще собранных")
            try:
                await bot.send_message(
                    update_images.order.user.user_id,
                    f"{hbold('💡Статус обновлен:')}\n"
                    f"{hbold('📄Опиcание:')} {db_obj_order.description}\n"
                    f"{hbold('❗️Статус:')} {Order.OrderStatusWork.assembled}\n\n"
                    f"{hbold('🚛Водитель:')} {update_images.user.last_name}",
                    reply_markup=await self._keyboard_service.order_details_keyboard(
                        order_id=db_obj_order.id
                    )
                )
            except BotBlocked as bt_blocked:
                logger.info(f"{update_images.order.user.last_name} - заблокировал бота | {bt_blocked}")
                logger.info("Зашли если нет вообще доставленных_1")
            if not images_assembled and not image_in_work:
                logger.info("Зашли если нет вообще доставленных_2")
                obj_in_order = {"order_status": Order.OrderStatusWork.delivered}
                try:
                    await bot.send_message(
                        update_images.order.user.user_id,
                        f"{hbold('💡Статус обновлен:')}\n"
                        f"{hbold('📄Опиcание:')} {db_obj_order.description}\n"
                        f"{hbold('❗️Статус:')} {Order.OrderStatusWork.delivered}\n\n"
                        f"{hbold('🚛Водитель:')} {update_images.user.last_name}",
                        reply_markup=await self._keyboard_service.order_details_keyboard(
                            order_id=db_obj_order.id
                        )
                    )
                except BotBlocked as bt_blocked:
                    logger.info(f"{update_images.order.user.last_name} - заблокировал бота | {bt_blocked}")

        try:
            await bot.send_photo(
                update_images.order.user.user_id,
                update_images.image,
                f"{hbold('💡Статус обновлен:')}\n"
                f"{hbold('📄Опиcание:')} {update_images.image_description}\n"
                f"{hbold('❗️Статус:')} {update_images.image_status}\n\n"
                f"{hbold('🚛Водитель:')} {update_images.user.last_name}")
        except BotBlocked as bt_blocked:
            logger.info(f"{update_images.order.user.last_name} - заблокировал бота | {bt_blocked}")

        return self._repository_order.update(
            db_obj=db_obj_order,
            obj_in=obj_in_order,
            commit=True
        )

    async def get_image_for_manager(self, order_id):
        return self._repository_images.list(order_id=order_id)

    async def update_images(self, edit_obj: str, edit_answer: str, image_id):
        db_obj = self._repository_images.get(id=image_id)
        obj_in = {}

        if edit_answer == "image_description":
            obj_in.update({"image_description": edit_obj})

        elif edit_answer == "image":
            obj_in.update({"image": edit_obj})

        return self._repository_images.update(
            db_obj=db_obj,
            obj_in=obj_in,
            commit=True
        )

    async def get_images_assembled_or_in_work(self):
        return self._repository_images.get_assembled_or_in_work_images()