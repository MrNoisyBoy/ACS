#!/usr/bin/env python3
"""
Проверка структуры проекта
"""

import os
import sys

REQUIRED_FILES = [
    "main.py",
    "config.yaml",
    "users.json",
    "constants.py",
    "requirements.txt",
    "run_system.bat",
    "core/__init__.py",
    "core/auth.py",
    "core/acl.py",
    "core/models.py",
    "storage/__init__.py",
    "storage/config_manager.py",
    "storage/user_repository.py",
    "utils/__init__.py",
    "utils/logger.py",
    "utils/file_operations.py"
]

print("="*60)
print("ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
print("="*60)

all_ok = True
for file_path in REQUIRED_FILES:
    if os.path.exists(file_path):
        print(f"✅ {file_path}")
    else:
        print(f"❌ {file_path} - ОТСУТСТВУЕТ")
        all_ok = False

print("="*60)
if all_ok:
    print("✅ Все файлы на месте!")
else:
    print("❌ Отсутствуют некоторые файлы")

# Проверяем импорты
print("\nПроверка импортов...")
try:
    from core.models import User, UserSession
    print("✅ core.models - OK")
except Exception as e:
    print(f"❌ core.models: {e}")

try:
    from core.auth import Authenticator
    print("✅ core.auth - OK")
except Exception as e:
    print(f"❌ core.auth: {e}")

try:
    from storage.user_repository import UserRepository
    print("✅ storage.user_repository - OK")
except Exception as e:
    print(f"❌ storage.user_repository: {e}")

print("="*60)
print("\nЕсли есть ошибки, создайте недостающие файлы.")