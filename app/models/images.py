import enum

from sqlalchemy import (
    String,
    Column,
    Integer,
    ForeignKey,
    Enum,
    Boolean
)
from sqlalchemy.orm import relationship
from app.db.base import Base


class Images(Base):
    __tablename__ = "images"

    class ImageStatus(enum.Enum):
        in_work = "В работе"
        assembled = "Собран"
        delivered = "Доставлен"

    id = Column(Integer, primary_key=True)
    order_id = Column(
        Integer,
        ForeignKey("order.id")
    )
    image = Column(String(40))
    image_description = Column(String(200), nullable=True)
    image_status = Column(Enum(ImageStatus), default=ImageStatus.in_work)
    refund_status = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("telegram_user.id"))
    refund_comment = Column(String(200), nullable=True)
    user = relationship("TelegramUser")
    order = relationship("Order")

    def __str__(self):
        return f"{self.id} {self.user_id} {self.order_id}"
