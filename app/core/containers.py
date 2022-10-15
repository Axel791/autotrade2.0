from dependency_injector import containers, providers

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


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    repository_telegram_user = providers.Singleton(RepositoryTelegramUser, model=TelegramUser)
    repository_order = providers.Singleton(RepositoryOrder, model=Order)
    repository_images = providers.Singleton(RepositoryImages, model=Images)
    repository_report = providers.Singleton(RepositoryReport, model=Report)

    validate_service = providers.Factory(ValidateInformationService)
    service_telegram_user = providers.Factory(
        TelegramUserService,
        repository_telegram_user=repository_telegram_user,
    )
