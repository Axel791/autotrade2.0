from .base import RepositoryBase
from app.models.order import Order


class RepositoryOrder(RepositoryBase[Order]):
    pass
