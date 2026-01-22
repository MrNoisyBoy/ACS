"""
Текстовые константы системы
"""

# Приветственные сообщения
WELCOME_TITLE = "СИСТЕМА УПРАВЛЕНИЯ ДОСТУПОМ"
WELCOME_SUBTITLE = "Версия 3.0 - Параметризованная система"

# Описания ролей
ROLE_DESCRIPTIONS = {
    "SYSADMIN": "👑 Системный администратор",
    "ADMIN": "👨‍💼 Администратор",
    "MANAGER": "📊 Менеджер",
    "DESIGNER": "🎨 Веб-дизайнер",
    "DEVELOPER": "💻 Разработчик",
    "ANALYST": "📈 Аналитик",
    "GUEST": "👤 Гость"
}

# Описания операций
OPERATION_DESCRIPTIONS = {
    "READ": "Чтение файлов",
    "WRITE": "Запись файлов",
    "DELETE": "Удаление файлов",
    "LIST": "Просмотр списка файлов",
    "CONFIG": "Настройка системы"
}

# Сообщения об ошибках
ERROR_INVALID_CREDENTIALS = "❌ Неверное имя пользователя или пароль"
ERROR_PERMISSION_DENIED = "❌ Доступ запрещен"
ERROR_FILE_NOT_FOUND = "❌ Файл не найден"
ERROR_SYSTEM = "❌ Системная ошибка"

# Успешные сообщения
SUCCESS_LOGIN = "✅ Успешный вход в систему"
SUCCESS_LOGOUT = "👋 Выход из системы выполнен"
SUCCESS_FILE_SAVED = "✅ Файл успешно сохранен"
SUCCESS_FILE_DELETED = "🗑️ Файл успешно удален"

# Меню
MENU_TITLE = "📋 ГЛАВНОЕ МЕНЮ"
MENU_OPTIONS = [
    "📁 Просмотреть доступные файлы",
    "📖 Прочитать файл",
    "✏️  Создать/изменить файл",
    "🗑️  Удалить файл",
    "ℹ️  Информация о правах",
    "👋 Выйти из системы",
    "❌ Завершить программу"
]

# Подсказки
PROMPT_USERNAME = "👤 Имя пользователя: "
PROMPT_PASSWORD = "🔑 Пароль: "
PROMPT_CHOICE = "Выберите действие: "
PROMPT_FILENAME = "Введите имя файла: "
PROMPT_FOLDER_CHOICE = "Выберите папку: "
PROMPT_FILE_CONTENT = "Введите содержимое файла (для завершения введите END):"

# Информационные сообщения
INFO_AVAILABLE_FILES = "📁 ДОСТУПНЫЕ ФАЙЛЫ:"
INFO_USER_ROLE = "🎭 Роль пользователя:"
INFO_PERMISSIONS = "✅ ДОСТУПНЫЕ ОПЕРАЦИИ:"
INFO_FOLDERS = "📁 ДОСТУПНЫЕ ПАПКИ:"

# Иконки
ICON_FOLDER = "📁"
ICON_FILE = "📄"
ICON_USER = "👤"
ICON_ROLE = "🎭"
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_WARNING = "⚠️"