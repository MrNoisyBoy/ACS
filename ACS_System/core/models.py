"""
Модели данных системы
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """Модель пользователя"""
    username: str
    password_hash: str
    role: str

    def verify_password(self, password: str) -> bool:
        """Проверка пароля (для обратной совместимости)"""
        return self.password_hash == password


@dataclass
class UserSession:
    """Сессия пользователя"""
    user: User
    login_time: Optional[str] = None

    def __post_init__(self):
        self.login_time = datetime.now().isoformat()


@dataclass
class FileObject:
    """Объект файла для контроля доступа"""
    path: str
    owner: Optional[str] = None
    permissions: Optional[str] = None