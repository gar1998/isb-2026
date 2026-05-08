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

if __name__ == "__main__":
    settings_file = "test_settings.json"

    settings_paths = {
        "initial_file": "data/input.txt",
        "encrypted_file": "data/encrypted.txt",
        "decrypted_file": "data/decrypted.txt",
        "symmetric_key_encrypted": "keys/seed_encrypted.txt",
        "public_key": "keys/public.pem",
        "private_key": "keys/private.pem"
    }

    try:
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings_paths, f, indent=4)
        print(f"Создан фиктивный файл настроек: {settings_file}")
    except Exception as e:
        print(f"Ошибка при создании файла настроек: {e}")

    if os.path.exists(settings_file):
        os.remove(settings_file)
        print(f"Удален {settings_file}")