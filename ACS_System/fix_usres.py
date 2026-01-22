#!/usr/bin/env python3
"""
Создание правильного users.json с MD5 хэшами
"""

import json
import hashlib

# Пользователи с их ролями
users_data = [
    {"username": "sysadmin", "role": "SYSADMIN"},
    {"username": "admin", "role": "ADMIN"},
    {"username": "manager", "role": "MANAGER"},
    {"username": "designer", "role": "DESIGNER"},
    {"username": "developer", "role": "DEVELOPER"},
    {"username": "analyst", "role": "ANALYST"},
    {"username": "guest", "role": "GUEST"}
]

# Создаем полные записи с MD5 хэшами
final_users = []
for user in users_data:
    username = user["username"]
    # Пароль = логин, хэшируем в MD5
    password_hash = hashlib.md5(username.encode('utf-8')).hexdigest()

    final_users.append({
        "username": username,
        "password_hash": password_hash,
        "role": user["role"]
    })

# Сохраняем в файл
with open('users.json', 'w', encoding='utf-8') as f:
    json.dump(final_users, f, indent=2, ensure_ascii=False)

print("✅ users.json создан с правильными MD5 хэшами!")
print("\nЛогины и пароли (пароль совпадает с логином):")
print("-" * 50)
for user in final_users:
    print(f"  {user['username']:12} / {user['username']:12}")
    print(f"    Хэш MD5: {user['password_hash']}")
    print()

print("\nПример для входа:")
print("  Логин: manager")
print("  Пароль: manager")