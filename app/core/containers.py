from dependency_injector import containers, providers

from app import redis_init
from app.core.config import Settings

from app.models.telegram_user import TelegramUser
from app.models.order import Order
from app.models.images import Images
from app.models.report import Report

from app.repository.telegram_user import RepositoryTelegramUser
from app.repository.order import RepositoryOrder
from app.repository.images import RepositoryImages
from app.repository.report import RepositoryReport

from app.services.validators import ValidateInformationService
from app.services.telegram_user import TelegramUserService
from app.services.order import OrderService
from app.services.images import ImagesService
from app.services.report import ReportService

from app.db.session import SyncSession

from app.utils.keyboards.form_inline_keyboard import FormInlineKeyboardService


class Container(containers.DeclarativeContainer):

    config = providers.Singleton(Settings)
    db = providers.Singleton(SyncSession, db_url=config.provided.SYNC_SQLALCHEMY_DATABASE_URI)

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser, session=db)
    repository_order = providers.Singleton(RepositoryOrder, model=Order, session=db)
    repository_images = providers.Singleton(RepositoryImages, model=Images, session=db)
    repository_report = providers.Singleton(RepositoryReport, model=Report, session=db)

    redis = providers.Resource(redis_init.init_redis_pool, host=config.provided.REDIS_HOST)

    keyboard_service = providers.Singleton(
        FormInlineKeyboardService,
        repository_telegram_user=repository_telegram_user
    )
    validate_service = providers.Singleton(ValidateInformationService)
    service_telegram_user = providers.Singleton(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user
    )
    images_service = providers.Singleton(
        ImagesService,
        repository_images=repository_images,
        repository_telegram_user=repository_telegram_user,
        repository_order=repository_order,
        keyboard_service=keyboard_service
    )
    order_service = providers.Singleton(
        OrderService,
        repository_telegram_user=repository_telegram_user,
        repository_order=repository_order
    )
    report_service = providers.Singleton(
        ReportService,
        repository_telegram_user=repository_telegram_user,
        repository_report=repository_report
    )

