#!/usr/bin/env python3
"""
СИСТЕМА УПРАВЛЕНИЯ ДОСТУПОМ - ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ
Создание, чтение, редактирование, удаление файлов
"""

import os
import sys
import json
import hashlib
from datetime import datetime
from pathlib import Path

# ========== КОНФИГУРАЦИЯ ==========
USERS_FILE = "users.json"
WORKSPACE_ROOT = "workspace"

# Папки для каждой роли
ROLE_FOLDERS = {
    "sysadmin": ["system", "backups", "logs", "reports", "design", "code", "analytics", "temp", "shared"],
    "admin": ["reports", "backups", "shared"],
    "manager": ["reports", "shared"],
    "designer": ["design", "shared"],
    "developer": ["code", "temp", "shared"],
    "analyst": ["reports", "analytics", "shared"],
    "guest": ["shared"]
}

# Права для каждой роли
ROLE_PERMISSIONS = {
    "sysadmin": ["read", "write", "delete", "list"],
    "admin": ["read", "write", "delete", "list"],
    "manager": ["read", "write", "list"],
    "designer": ["read", "write", "list"],
    "developer": ["read", "write", "list"],
    "analyst": ["read", "list"],
    "guest": ["read"]
}


# ========== СИСТЕМА ==========

class User:
    def __init__(self, username, password_hash, role):
        self.username = username
        self.password_hash = password_hash
        self.role = role


class ACSystem:
    def __init__(self):
        self.current_user = None
        self.load_users()
        self.setup_workspace()

    def load_users(self):
        """Загрузка пользователей из JSON"""
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users_data = json.load(f)

            self.users = {}
            for user_data in users_data:
                user = User(
                    username=user_data['username'],
                    password_hash=user_data['password_hash'],
                    role=user_data['role']
                )
                self.users[user.username] = user

            print(f"✅ Загружено {len(self.users)} пользователей")
        except Exception as e:
            print(f"❌ Ошибка загрузки users.json: {e}")
            sys.exit(1)

    def setup_workspace(self):
        """Настройка рабочей директории"""
        os.makedirs(WORKSPACE_ROOT, exist_ok=True)

        # Создаем системные папки
        all_folders = set()
        for folders in ROLE_FOLDERS.values():
            all_folders.update(folders)

        for folder in all_folders:
            os.makedirs(f"{WORKSPACE_ROOT}/{folder}", exist_ok=True)

        # Создаем личные папки
        for username in self.users.keys():
            os.makedirs(f"{WORKSPACE_ROOT}/user_{username}", exist_ok=True)

        # Создаем тестовые файлы
        self.create_sample_files()

    def create_sample_files(self):
        """Создание тестовых файлов"""
        sample_files = {
            "reports": [
                ("monthly_report.txt", "Отчет за месяц\nПрибыль: 1,500,000 руб.\n"),
                ("sales.csv", "Дата,Товар,Количество,Сумма\n2024-01-15,Товар А,100,500000\n")
            ],
            "design": [
                ("prototype.fig", "Прототип сайта компании\n"),
                ("styles.css", "/* Основные стили */\nbody { font-family: Arial; }\n")
            ],
            "code": [
                ("main.py", "#!/usr/bin/env python3\nprint('Hello ACS System!')\n"),
                ("config.json", '{"version": "1.0", "debug": true}\n')
            ],
            "shared": [
                ("welcome.txt", "Добро пожаловать в общую папку!\n"),
                ("contacts.txt", "IT поддержка: 1111\nБухгалтерия: 2222\n")
            ]
        }

        for folder, files in sample_files.items():
            for filename, content in files:
                filepath = f"{WORKSPACE_ROOT}/{folder}/{filename}"
                if not os.path.exists(filepath):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)

        # Создаем личные файлы для пользователей
        for username in self.users.keys():
            filepath = f"{WORKSPACE_ROOT}/user_{username}/readme.txt"
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"Личная папка пользователя {username}\n")
                    f.write(f"Роль: {self.users[username].role}\n")
                    f.write("Здесь вы можете создавать свои файлы.\n")

    def login(self):
        """Вход в систему"""
        print("\n" + "=" * 60)
        print("СИСТЕМА УПРАВЛЕНИЯ ДОСТУПОМ".center(60))
        print("=" * 60)

        print("\n👥 ДОСТУПНЫЕ ПОЛЬЗОВАТЕЛИ (пароль = логин):")
        print("-" * 50)
        for username, user in self.users.items():
            print(f"  {username:12} - {user.role}")
        print("-" * 50)

        attempts = 3
        while attempts > 0:
            print(f"\n[Попыток: {attempts}]")
            username = input("👤 Логин: ").strip()
            password = input("🔒 Пароль: ").strip()

            if username in self.users:
                user = self.users[username]
                # Проверяем пароль (MD5 хэш)
                input_hash = hashlib.md5(password.encode()).hexdigest()

                if input_hash == user.password_hash:
                    self.current_user = user
                    print(f"\n✅ УСПЕШНЫЙ ВХОД!")
                    print(f"   Пользователь: {username}")
                    print(f"   Роль: {user.role}")
                    return True
                else:
                    print("❌ Неверный пароль!")
            else:
                print("❌ Пользователь не найден!")

            attempts -= 1

        print("\n🚫 Доступ запрещен!")
        return False

    def can_do(self, action):
        """Проверка прав"""
        return action in ROLE_PERMISSIONS.get(self.current_user.role, [])

    def get_accessible_files(self):
        """Получить список доступных файлов"""
        files = []

        # Личная папка
        user_folder = f"{WORKSPACE_ROOT}/user_{self.current_user.username}"
        if os.path.exists(user_folder):
            for filename in os.listdir(user_folder):
                filepath = os.path.join(user_folder, filename)
                if os.path.isfile(filepath):
                    files.append({
                        'path': filepath,
                        'name': filename,
                        'folder': f"user_{self.current_user.username}",
                        'type': 'personal'
                    })

        # Системные папки
        folders = ROLE_FOLDERS.get(self.current_user.role, [])
        for folder in folders:
            folder_path = f"{WORKSPACE_ROOT}/{folder}"
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    filepath = os.path.join(folder_path, filename)
                    if os.path.isfile(filepath):
                        files.append({
                            'path': filepath,
                            'name': filename,
                            'folder': folder,
                            'type': 'system'
                        })

        return files

    def show_files(self):
        """Показать доступные файлы"""
        if not self.can_do("list"):
            print("❌ Нет прав на просмотр файлов")
            return []

        files = self.get_accessible_files()

        if not files:
            print("\n📭 Нет доступных файлов")
            return []

        print(f"\n📁 ДОСТУПНЫЕ ФАЙЛЫ ({len(files)} шт.):")
        print("-" * 60)

        # Группируем по папкам
        folders = {}
        for file in files:
            folder = file['folder']
            if folder not in folders:
                folders[folder] = []
            folders[folder].append(file)

        for folder, folder_files in folders.items():
            print(f"\n📂 {folder}/:")
            for i, file in enumerate(folder_files, 1):
                size = os.path.getsize(file['path'])
                print(f"  {i:2}. 📄 {file['name']} ({size} байт)")

        return files

    def read_file(self):
        """Чтение файла"""
        if not self.can_do("read"):
            print("❌ Нет прав на чтение")
            return

        files = self.show_files()
        if not files:
            return

        try:
            choice = input(f"\nВыберите файл для чтения (1-{len(files)}): ").strip()
            if not choice.isdigit():
                print("❌ Введите число!")
                return

            index = int(choice) - 1
            if 0 <= index < len(files):
                file = files[index]

                with open(file['path'], 'r', encoding='utf-8') as f:
                    content = f.read()

                print(f"\n📖 СОДЕРЖИМОЕ: {file['folder']}/{file['name']}")
                print("=" * 60)
                print(content)
                print("=" * 60)
            else:
                print("❌ Неверный номер файла")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def edit_file(self):
        """Редактирование файла"""
        if not self.can_do("write"):
            print("❌ Нет прав на запись")
            return

        files = self.get_accessible_files()
        if not files:
            print("❌ Нет доступных файлов")
            return

        # Показываем только файлы доступные для записи
        writable_files = []
        for file in files:
            if file['type'] == 'personal':
                writable_files.append(file)
            elif file['folder'] in ROLE_FOLDERS.get(self.current_user.role, []):
                writable_files.append(file)

        if not writable_files:
            print("❌ Нет файлов доступных для редактирования")
            return

        print("\n✏️  ВЫБЕРИТЕ ФАЙЛ ДЛЯ РЕДАКТИРОВАНИЯ:")
        for i, file in enumerate(writable_files, 1):
            print(f"{i:2}. {file['folder']}/{file['name']}")

        try:
            choice = input(f"\nНомер файла (1-{len(writable_files)}): ").strip()
            if not choice.isdigit():
                print("❌ Введите число!")
                return

            index = int(choice) - 1
            if 0 <= index < len(writable_files):
                file = writable_files[index]

                # Читаем текущее содержимое
                with open(file['path'], 'r', encoding='utf-8') as f:
                    current_content = f.read()

                print(f"\n📝 РЕДАКТИРОВАНИЕ: {file['name']}")
                print("Текущее содержимое:")
                print("-" * 40)
                print(current_content)
                print("-" * 40)

                # Вводим новое содержимое
                print("\nВведите новое содержимое (END для завершения):")
                print("-" * 40)

                lines = []
                line_num = 1
                while True:
                    try:
                        line = input(f"{line_num:3}> ")
                        if line.upper() == "END":
                            break
                        lines.append(line)
                        line_num += 1
                    except EOFError:
                        break

                new_content = "\n".join(lines)

                if new_content.strip() == "":
                    print("❌ Содержимое не может быть пустым")
                    return

                # Сохраняем
                with open(file['path'], 'w', encoding='utf-8') as f:
                    f.write(new_content)

                print(f"\n✅ Файл успешно отредактирован!")

            else:
                print("❌ Неверный номер файла")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def create_file(self):
        """Создание нового файла"""
        if not self.can_do("write"):
            print("❌ Нет прав на запись")
            return

        print("\n📝 СОЗДАНИЕ НОВОГО ФАЙЛА")
        print("-" * 40)

        # Выбор папки
        available_folders = []

        # Личная папка всегда доступна
        personal_folder = f"{WORKSPACE_ROOT}/user_{self.current_user.username}"
        available_folders.append(("📁 Личная папка", personal_folder))

        # Системные папки доступные для записи
        system_folders = ROLE_FOLDERS.get(self.current_user.role, [])
        for folder in system_folders:
            if folder != "shared":  # Общую папку не показываем для создания
                folder_path = f"{WORKSPACE_ROOT}/{folder}"
                available_folders.append((f"📂 {folder}", folder_path))

        print("\nВыберите папку:")
        for i, (name, path) in enumerate(available_folders, 1):
            print(f"{i}. {name}")

        try:
            choice = input(f"\nНомер папки (1-{len(available_folders)}): ").strip()
            if not choice.isdigit():
                print("❌ Введите число!")
                return

            index = int(choice) - 1
            if 0 <= index < len(available_folders):
                folder_name, folder_path = available_folders[index]

                filename = input("\nИмя файла (с расширением): ").strip()
                if not filename:
                    print("❌ Имя файла не может быть пустым")
                    return

                # Проверяем имя файла
                invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
                for char in invalid_chars:
                    if char in filename:
                        print(f"❌ Недопустимый символ в имени файла: {char}")
                        return

                filepath = os.path.join(folder_path, filename)

                # Ввод содержимого
                print("\nВведите содержимое файла (END для завершения):")
                print("-" * 40)

                lines = []
                line_num = 1
                while True:
                    try:
                        line = input(f"{line_num:3}> ")
                        if line.upper() == "END":
                            break
                        lines.append(line)
                        line_num += 1
                    except EOFError:
                        break

                content = "\n".join(lines)

                if content.strip() == "":
                    content = f"Файл создан: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                    content += f"Пользователь: {self.current_user.username}\n"
                    content += f"Роль: {self.current_user.role}\n"

                # Создаем файл
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"\n✅ Файл успешно создан!")
                print(f"   Путь: {os.path.relpath(filepath, WORKSPACE_ROOT)}")

            else:
                print("❌ Неверный номер папки")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def delete_file(self):
        """Удаление файла"""
        if not self.can_do("delete"):
            print("❌ Нет прав на удаление")
            return

        files = self.get_accessible_files()
        if not files:
            print("❌ Нет доступных файлов")
            return

        # Показываем файлы доступные для удаления
        deletable_files = []
        for file in files:
            if file['type'] == 'personal':
                deletable_files.append(file)
            elif self.current_user.role == "sysadmin":
                deletable_files.append(file)

        if not deletable_files:
            print("❌ Нет файлов доступных для удаления")
            return

        print("\n🗑️  ВЫБЕРИТЕ ФАЙЛ ДЛЯ УДАЛЕНИЯ:")
        for i, file in enumerate(deletable_files, 1):
            print(f"{i:2}. {file['folder']}/{file['name']}")

        try:
            choice = input(f"\nНомер файла (1-{len(deletable_files)}): ").strip()
            if not choice.isdigit():
                print("❌ Введите число!")
                return

            index = int(choice) - 1
            if 0 <= index < len(deletable_files):
                file = deletable_files[index]

                # Подтверждение
                print(f"\n⚠️  ВНИМАНИЕ: Вы собираетесь удалить файл")
                print(f"   {file['folder']}/{file['name']}")
                confirm = input("\nПодтвердите удаление (введите 'УДАЛИТЬ'): ").strip()

                if confirm == "УДАЛИТЬ":
                    os.remove(file['path'])
                    print(f"\n✅ Файл успешно удален!")
                else:
                    print("❌ Удаление отменено")
            else:
                print("❌ Неверный номер файла")

        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def show_menu(self):
        """Главное меню"""
        print(f"\n{'=' * 60}")
        print(f"👤 Пользователь: {self.current_user.username}")
        print(f"🎭 Роль: {self.current_user.role}")
        print("=" * 60)

        print("\n📋 ГЛАВНОЕ МЕНЮ:")
        print("1. 📁 Показать доступные файлы")
        print("2. 📖 Прочитать файл")
        print("3. ✏️  Редактировать файл")
        print("4. 📝 Создать новый файл")
        print("5. 🗑️  Удалить файл")
        print("6. ℹ️  Информация о системе")
        print("7. 👋 Выйти из системы")
        print("0. ❌ Завершить программу")

    def show_system_info(self):
        """Информация о системе"""
        print(f"\n{'=' * 60}")
        print("ℹ️  ИНФОРМАЦИЯ О СИСТЕМЕ")
        print("=" * 60)

        print(f"\n👤 Пользователь: {self.current_user.username}")
        print(f"🎭 Роль: {self.current_user.role}")

        print(f"\n✅ Ваши права:")
        for perm in ROLE_PERMISSIONS.get(self.current_user.role, []):
            print(f"  • {perm}")

        print(f"\n📁 Доступные папки:")
        for folder in ROLE_FOLDERS.get(self.current_user.role, []):
            print(f"  • {folder}/")

        # Статистика
        total_files = 0
        for root, dirs, files in os.walk(WORKSPACE_ROOT):
            total_files += len(files)

        print(f"\n📊 Всего файлов в системе: {total_files}")
        print(f"💾 Рабочая директория: {WORKSPACE_ROOT}/")
        print("=" * 60)

    def run(self):
        """Запуск системы"""
        if not self.login():
            return

        while True:
            try:
                self.show_menu()
                choice = input("\nВыберите действие (0-7): ").strip()

                if choice == "1":
                    self.show_files()
                elif choice == "2":
                    self.read_file()
                elif choice == "3":
                    self.edit_file()
                elif choice == "4":
                    self.create_file()
                elif choice == "5":
                    self.delete_file()
                elif choice == "6":
                    self.show_system_info()
                elif choice == "7":
                    print(f"\n👋 Выход из системы...")
                    self.current_user = None
                    return True  # Вернуться к логину
                elif choice == "0":
                    print(f"\n❌ Завершение работы...")
                    return False  # Завершить программу
                else:
                    print("❌ Неверный выбор")

                input("\n↵ Нажмите Enter для продолжения...")

            except KeyboardInterrupt:
                print("\n\n⚠ Прервано пользователем")
                return False
            except Exception as e:
                print(f"\n❌ Ошибка: {e}")
                continue


def main():
    """Главная функция"""
    print("🚀 Запуск системы управления доступом...")

    system = ACSystem()

    while True:
        try:
            continue_program = system.run()
            if not continue_program:
                break
        except KeyboardInterrupt:
            print("\n\n👋 Завершение работы")
            break
        except Exception as e:
            print(f"\n❌ Критическая ошибка: {e}")
            break

    print("\n✅ Работа системы завершена")
    print(f"📁 Все файлы сохранены в папке '{WORKSPACE_ROOT}/'")
    input("\n↵ Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()