import enum

from sqlalchemy import String, Column, Integer, Enum
from app.db.base import Base


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    class WorkingStatus(enum.Enum):
        worked = "Работает"
        on_vacation = "В отпуске"
        dismissed = "Уволен/Уволился"

    class PermissionStatus(enum.Enum):
        driver = "Водитель"
        financier = "Финансист"
        accountant = "Бухгалтер"
        manager = "Менеджер"
        super_user = "Супер-пользователь"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    username = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    patronymic = Column(String(50), nullable=True)
    phone_number = Column(String(13), nullable=True)
    working_status = Column(Enum(WorkingStatus), nullable=True)
    permission_status = Column(Enum(PermissionStatus), nullable=True)

    def __str__(self):
        return f"{self.username} {self.first_name} {self.user_id}"




