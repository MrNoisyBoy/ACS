"""
Менеджер конфигурации - чтение параметров из YAML
"""

import yaml
import os
from pathlib import Path

class ConfigManager:
    """Управление конфигурацией системы"""

    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = Path(config_file)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Загрузка конфигурации из YAML"""
        try:
            if not self.config_file.exists():
                raise FileNotFoundError(f"Конфигурационный файл {self.config_file} не найден")

            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            return config

        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            raise

    def get_workspace_root(self) -> str:
        """Получение пути к рабочей директории"""
        workspace_root = self.config.get('system', {}).get('workspace_root', './workspace')

        # Преобразуем в абсолютный путь
        if not os.path.isabs(workspace_root):
            base_dir = Path(__file__).parent.parent
            workspace_root = str(base_dir / workspace_root)

        return os.path.normpath(workspace_root)

    def get_log_config(self) -> dict:
        """Получение конфигурации логирования"""
        return self.config.get('system', {})

    def get_roles_config(self) -> dict:
        """Получение конфигурации ролей"""
        return self.config.get('roles', {})

    def get_folder_names(self) -> dict:
        """Получение названий папок"""
        return self.config.get('folders', {})

    def get_role_permissions(self, role: str) -> list:
        """Получение прав для роли"""
        role_config = self.config.get('roles', {}).get(role, {})
        return role_config.get('permissions', [])

    def get_role_folders(self, role: str) -> list:
        """Получение папок для роли"""
        role_config = self.config.get('roles', {}).get(role, {})
        return role_config.get('folders', [])