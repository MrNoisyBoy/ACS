"""
Репозиторий пользователей - загрузка из JSON
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, List
from core.models import User

class UserRepository:
    """Хранилище данных пользователей"""

    def __init__(self, logger, users_file: str = "users.json"):
        self.logger = logger
        self.users_file = Path(users_file)
        self.users = self._load_users()

    def _load_users(self) -> dict:
        """Загрузка пользователей из JSON файла"""
        try:
            self.logger.info(f"Загрузка пользователей из {self.users_file}")

            if not self.users_file.exists():
                self.logger.error(f"Файл пользователей не найден: {self.users_file}")
                raise FileNotFoundError(f"Файл пользователей не найден: {self.users_file}")

            with open(self.users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)

            users = {}
            for user_data in users_data:
                user = User(
                    username=user_data['username'],
                    password_hash=user_data['password_hash'],
                    role=user_data['role']
                )
                users[user.username] = user

            self.logger.info(f"Загружено {len(users)} пользователей")
            return users

        except Exception as e:
            self.logger.error(f"Ошибка загрузки пользователей: {e}")
            return {}

    def get_user(self, username: str) -> Optional[User]:
        """Получение пользователя по имени"""
        return self.users.get(username)

    def get_all_users(self) -> List[User]:
        """Получение всех пользователей"""
        return list(self.users.values())

    def verify_password(self, username: str, password: str) -> bool:
        """Проверка пароля"""
        user = self.get_user(username)
        if not user:
            return False

        # Хэшируем введенный пароль и сравниваем
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return user.password_hash == password_hash