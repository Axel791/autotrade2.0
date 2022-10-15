import datetime
import enum

from sqlalchemy import (
    String,
    Column,
    Integer,
    ForeignKey,
    Enum,
    DateTime
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Order(Base):
    __tablename__ = "order"

    class OrderStatusWork(enum.Enum):
        in_work = "В работе"
        partially_assembled = "Частично собран"
        assembled = "Собран"
        delivered = "Доставлен"

    class OrderStatusRefund(enum.Enum):
        activity = "Активный"
        partially_refund = "Частичный возврат"
        refund = "Возрат"

    class PaymentType(enum.Enum):
        cash = "Наличные"
        non_cash = "Безналичные"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("telegram_user.id")
    )
    description = Column(String(2000), nullable=False)
    purchase_count = Column(Integer, default=0)
    sale_count = Column(Integer, default=0)
    order_status = Column(Enum(OrderStatusWork), default=OrderStatusWork.in_work)
    refund_status = Column(Enum(OrderStatusRefund), default=OrderStatusRefund.activity)
    refund_comment = Column(String(300), nullable=True)
    payment_type = Column(Enum(PaymentType))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("TelegramUser")

    def __str__(self):
        return f"{self.id} {self.user}"


