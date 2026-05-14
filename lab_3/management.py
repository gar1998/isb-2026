
import json
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def read_json_file(json_file : str) -> tuple[dict[str, str] | None, str | None]:
    """
    Чтение JSON-файла
    :param json_file: Путь к JSON-файлу
    :return: Данные из JSON-файла и сообщение об ошибке
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            return json_data, None
    except FileNotFoundError as e:
        return None, f"Ошибка: Запрашиваемый файл формата json не найден '{json_file}': {e}"

def load_settings(settings_file : str = "settings.json")->tuple[dict[str, str] | None, str | None]:
    """
    Загружает настройки из JSON-файла
    Если файл не найден или неполный, возвращает None и сообщение об ошибке
    :param settings_file: JSON-файл с необходимыми настройками
    :return: полученные настройки и сообщение об ошибке - пустое если всё хорошо
    """

    settings = read_json_file(settings_file)
    if settings is None:
        return None, f"Файл с настройками {settings_file} пуст"

    return settings


def write_in_file_pem(path : str, pem : bytes)->None:
    """
    Запись в pem файл
    :param path: Путь к файлу
    :param pem: Формат ключа
    :return: Ничего
    """
    try:
        with open(path, 'wb') as f:
            f.write(pem)
    except FileNotFoundError as e:
        print(f"Ошибка: файл {path} не найден")


def read_pem_file(path : str)->rsa.RSAPrivateKey | rsa.RSAPublicKey:
    """
    Чтение pem файла
    :param path: Путь к файлу
    :return: RSA ключ (открытый или закрытый)
    """
    try:
        with open(path, 'rb') as f:
            key = serialization.load_pem_private_key(f.read(), password=None)
        return key
    except FileNotFoundError as e:
        print(f"Ошибка: файл {path} не найден")

def read_and_write_in_file(path : str, mode : str, data : bytes = None)-> None | bytes:
    """
    Чтение или запись в файл
    :param path: Путь к файлу
    :param mode: Режим работы с файлом
    :param data: Данные для запись в файл (необязательно)
    :return: Прочитанные данные либо ничего
    """
    try:
        with open(path, mode) as f:
            if mode == 'wb':
                f.write(data)
            if mode == 'rb':
                info = f.read()
                return info
    except FileNotFoundError as e:
        print(f"Ошибка: файл {path} не найден")