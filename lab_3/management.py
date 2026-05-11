import os
import json
from constants import REQUIRED_SETTINGS_KEYS


def load_settings(settings_file : str = "settings.json")->tuple[dict[str, str] | None, str | None]:
    """
    Загружает настройки из JSON-файла
    Если файл не найден или неполный, возвращает None и сообщение об ошибке
    :param settings_file: JSON-файл с необходимыми настройками
    :return: полученные настройки и сообщение об ошибке - пустое если всё хорошо
    """

    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError as e:
        return None, f"Ошибка: Запрашиваемый файл формата json не найден '{settings_file}': {e}"

    missing_keys = []
    for key in REQUIRED_SETTINGS_KEYS:
        if key not in settings:
            missing_keys.append(key)

    if missing_keys:
        return None, (
            f"Ошибка: В файле '{settings_file}' отсутствуют следующие обязательные настройки: {', '.join(missing_keys)}\n"
            "Убедитесь, что 'settings.json' содержит все необходимые пути"
        )


    for key, path in settings.items():
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
                print(f"Создана директория: {dirname}")
            except OSError as e:
                return None, f"Ошибка при создании директории {dirname}: {e}"

    return settings, None

