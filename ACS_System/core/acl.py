"""
Контроль доступа - параметризованная версия
"""

import os
from pathlib import Path
from typing import List
import constants as const

class AccessController:
    """Контроллер доступа на основе ролей"""

    def __init__(self, config_manager, logger):
        self.config = config_manager
        self.logger = logger
        self.workspace_root = config_manager.get_workspace_root()
        self.roles_config = config_manager.get_roles_config()

    def check_permission(self, user_role: str, operation: str, filepath: str = None) -> bool:
        """Проверка прав доступа"""

        # Получаем права для роли из конфигурации
        role_config = self.roles_config.get(user_role, {})
        permissions = role_config.get('permissions', [])

        if operation not in permissions:
            self.logger.warning(f"Роль {user_role} не имеет права {operation}")
            return False

        # Если файл не указан - проверяем только операцию
        if not filepath:
            return True

        # Проверяем доступ к конкретному файлу
        return self._check_file_access(user_role, operation, filepath)

    def _check_file_access(self, user_role: str, operation: str, filepath: str) -> bool:
        """Проверка доступа к файлу"""

        try:
            # Приводим путь к относительному относительно workspace
            rel_path = Path(filepath).relative_to(self.workspace_root)
        except ValueError:
            # Файл вне workspace - доступ запрещен
            return False

        parts = rel_path.parts

        # Личная папка пользователя (определяется по имени файла в main.py)
        if parts[0].startswith("user_"):
            # Валидация происходит в основном коде
            return True

        # Проверяем доступ к системным папкам
        if len(parts) > 0:
            folder = parts[0]
            role_folders = self.config.get_role_folders(user_role)

            if folder in role_folders:
                return True

        return False

    def get_accessible_folders(self, user_role: str) -> List[str]:
        """Получение доступных папок для роли"""
        return self.config.get_role_folders(user_role)