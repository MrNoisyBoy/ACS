#!/usr/bin/env python3
"""
Проверка паролей в users.json
"""

import json
import hashlib


def check_all_passwords():
    """Проверить все пароли"""
    with open('users.json', 'r', encoding='utf-8') as f:
        users = json.load(f)

    print("Проверка паролей в users.json:")
    print("-" * 60)

    all_correct = True
    for user in users:
        username = user['username']
        stored_hash = user['password_hash']

        # Пароль должен совпадать с логином
        expected_hash = hashlib.md5(username.encode()).hexdigest()

        if stored_hash == expected_hash:
            print(f"✅ {username:12} - OK (пароль: {username})")
        else:
            print(f"❌ {username:12} - ОШИБКА!")
            print(f"   Ожидался: {expected_hash}")
            print(f"   В файле:  {stored_hash}")
            all_correct = False

    print("-" * 60)
    if all_correct:
        print("✅ Все пароли верны!")
    else:
        print("❌ Есть ошибки в паролях!")


if __name__ == "__main__":
    check_all_passwords()