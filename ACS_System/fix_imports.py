#!/usr/bin/env python3
"""
Создание недостающих файлов
"""

import os

# Создаем недостающие файлы
files_to_create = {
    "core/models.py": '''
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
''',

    "core/__init__.py": "# Ядро системы\n",

    "storage/__init__.py": "# Хранилища данных\n",

    "utils/__init__.py": "# Утилиты системы\n"
}

# Создаем папки
os.makedirs("core", exist_ok=True)
os.makedirs("storage", exist_ok=True)
os.makedirs("utils", exist_ok=True)

# Создаем файлы
for filepath, content in files_to_create.items():
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Создан: {filepath}")
    else:
        print(f"✓ Уже существует: {filepath}")

print("\n✅ Структура проекта исправлена!")
print("Запустите: python check_structure.py")