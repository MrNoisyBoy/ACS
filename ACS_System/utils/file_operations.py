"""
Операции с файлами с проверкой прав доступа
Включает создание, чтение, редактирование и удаление
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
import constants as const

class FileOperations:
    """Класс для безопасных операций с файлами"""

    def __init__(self, config_manager, access_controller, user_session, logger):
        self.config = config_manager
        self.acl = access_controller
        self.session = user_session
        self.logger = logger
        self.workspace_root = config_manager.get_workspace_root()

    def list_accessible_files(self) -> List[dict]:
        """Получить список доступных файлов"""
        accessible_files = []

        # Личная папка пользователя
        user_folder = os.path.join(self.workspace_root, f"user_{self.session.user.username}")
        if os.path.exists(user_folder):
            accessible_files.extend(self._get_files_in_folder(user_folder, "Личная папка"))

        # Системные папки доступные пользователю
        role_folders = self.config.get_role_folders(self.session.user.role)
        for folder_name in role_folders:
            folder_path = os.path.join(self.workspace_root, folder_name)
            if os.path.exists(folder_path):
                folder_display = self.config.get_folder_names().get(folder_name, folder_name)
                accessible_files.extend(self._get_files_in_folder(folder_path, folder_display))

        return accessible_files

    def _get_files_in_folder(self, folder_path: str, folder_name: str) -> List[dict]:
        """Получить файлы в папке"""
        files = []

        try:
            for filename in os.listdir(folder_path):
                filepath = os.path.join(folder_path, filename)
                if os.path.isfile(filepath):
                    files.append({
                        'path': filepath,
                        'name': filename,
                        'folder': folder_name,
                        'size': os.path.getsize(filepath)
                    })
        except PermissionError:
            self.logger.warning(f"Нет доступа к папке: {folder_path}")

        return files

    def read_file(self, filepath: str) -> str:
        """Прочитать содержимое файла"""
        if not self.acl.check_permission(self.session.user.role, "READ", filepath):
            raise PermissionError(const.ERROR_PERMISSION_DENIED)

        if not os.path.exists(filepath):
            raise FileNotFoundError(const.ERROR_FILE_NOT_FOUND)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            rel_path = os.path.relpath(filepath, self.workspace_root)
            self.logger.info(f"Пользователь {self.session.user.username} прочитал файл: {rel_path}")

            return content

        except UnicodeDecodeError:
            raise ValueError("Файл содержит бинарные данные")

    def write_file(self, filepath: str, content: str, mode: str = 'w') -> bool:
        """Записать или создать файл"""
        if not self.acl.check_permission(self.session.user.role, "WRITE", filepath):
            raise PermissionError(const.ERROR_PERMISSION_DENIED)

        # Проверяем, можно ли писать в эту папку
        folder_name = os.path.basename(os.path.dirname(filepath))
        if not folder_name.startswith("user_"):  # Не личная папка
            role_folders = self.config.get_role_folders(self.session.user.role)
            if folder_name not in role_folders:
                raise PermissionError(f"Нет прав на запись в папку '{folder_name}'")

        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        try:
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)

            rel_path = os.path.relpath(filepath, self.workspace_root)
            self.logger.info(f"Пользователь {self.session.user.username} записал файл: {rel_path}")

            return True

        except Exception as e:
            self.logger.error(f"Ошибка записи файла {filepath}: {e}")
            raise

    def edit_file(self, filepath: str) -> bool:
        """Редактировать существующий файл"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(const.ERROR_FILE_NOT_FOUND)

        if not self.acl.check_permission(self.session.user.role, "WRITE", filepath):
            raise PermissionError(const.ERROR_PERMISSION_DENIED)

        # Читаем текущее содержимое
        current_content = self.read_file(filepath)

        print(f"\n📝 Редактирование файла: {os.path.basename(filepath)}")
        print("Текущее содержимое:")
        print("-" * 40)
        print(current_content)
        print("-" * 40)

        # Запрашиваем новое содержимое
        print("\nВведите новое содержимое (для завершения введите END на новой строке):")
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
                print("\nРедактирование прервано")
                return False

        new_content = "\n".join(lines)

        if new_content.strip() == "":
            print("❌ Содержимое не может быть пустым")
            return False

        # Сохраняем изменения
        return self.write_file(filepath, new_content, 'w')

    def delete_file(self, filepath: str) -> bool:
        """Удалить файл"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(const.ERROR_FILE_NOT_FOUND)

        if not self.acl.check_permission(self.session.user.role, "DELETE", filepath):
            raise PermissionError(const.ERROR_PERMISSION_DENIED)

        # Для безопасности - проверяем что файл в workspace
        try:
            rel_path = os.path.relpath(filepath, self.workspace_root)
        except ValueError:
            raise PermissionError("Нельзя удалять файлы вне рабочей директории")

        # Подтверждение
        print(f"\n❓ Вы уверены, что хотите удалить файл '{rel_path}'?")
        confirm = input("Введите 'ДА' для подтверждения: ").strip().upper()

        if confirm == "ДА":
            try:
                os.remove(filepath)
                self.logger.warning(f"Пользователь {self.session.user.username} удалил файл: {rel_path}")
                return True
            except Exception as e:
                self.logger.error(f"Ошибка удаления файла {filepath}: {e}")
                raise
        else:
            print("❌ Удаление отменено")
            return False

    def create_file(self, folder_path: str, filename: str, content: str = "") -> str:
        """Создать новый файл"""
        filepath = os.path.join(folder_path, filename)

        if not self.acl.check_permission(self.session.user.role, "WRITE", filepath):
            raise PermissionError(const.ERROR_PERMISSION_DENIED)

        # Проверяем расширение файла
        if not self._is_valid_filename(filename):
            raise ValueError("Некорректное имя файла")

        # Создаем файл
        if content == "":
            content = f"Файл создан пользователем: {self.session.user.username}\n"
            content += f"Роль: {self.session.user.role}\n"
            content += f"Дата создания: {self._get_current_timestamp()}\n"

        self.write_file(filepath, content, 'w')

        return os.path.relpath(filepath, self.workspace_root)

    def _is_valid_filename(self, filename: str) -> bool:
        """Проверка корректности имени файла"""
        if not filename or filename.strip() == "":
            return False

        # Запрещенные символы
        invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '\\', '/']
        for char in invalid_chars:
            if char in filename:
                return False

        return True

    def _get_current_timestamp(self) -> str:
        """Получить текущую дату и время"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")