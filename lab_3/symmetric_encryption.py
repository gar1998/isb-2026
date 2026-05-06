import os

from constants import SEED_KEY_LENGTH


def generate_seed_key()->bytes:
    """
    Генерирует случайный 128-битный симметричный SEED ключ
    :return: 128-битный симметричный SEED ключ
    """
    print("Генерация SEED ключа...")

    key = os.urandom(SEED_KEY_LENGTH)

    print("SEED ключ сгенерирован")
    return key

if __name__ == "__main__":
    key = generate_seed_key()
    print(f"Сгенерированный ключ: {key.hex()}")
    print(f"Длина ключа: {len(key)} байт")s