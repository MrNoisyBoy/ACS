import hashlib
from typing import Optional
from core.models import User

class Authenticator:
    """Аутентификация с проверкой MD5 хэшей"""

    def __init__(self, user_repository, logger):
        self.user_repo = user_repository
        self.logger = logger

    def hash_password(self, password: str) -> str:
        """Хэширование пароля MD5"""
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        try:
            self.logger.debug(f"Аутентификация пользователя: {username}")

            # Получаем пользователя
            user = self.user_repo.get_user(username)
            if not user:
                self.logger.warning(f"Пользователь не найден: {username}")
                return None

            # Хэшируем введенный пароль и сравниваем
            password_hash = self.hash_password(password)

            if user.password_hash == password_hash:
                self.logger.info(f"Успешная аутентификация: {username}")
                return user
            else:
                self.logger.warning(f"Неверный пароль для пользователя: {username}")
                return None

        except Exception as e:
            self.logger.error(f"Ошибка аутентификации: {e}")
            return None