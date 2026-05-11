import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag

from constants import SEED_KEY_LENGTH, SEED_BLOCK_SIZE


def generate_seed_key()->bytes:
    """
    Генерирует случайный 128-битный симметричный SEED ключ
    :return: 128-битный симметричный SEED ключ
    """
    print("Генерация SEED ключа...")

    key = os.urandom(SEED_KEY_LENGTH)

    print("SEED ключ сгенерирован")
    return key

def encrypt_file_seed(input_filepath : str, output_filepath : str, seed_key : bytes)->bool:
    """
    Шифрует файл с использованием SEED в режиме CBC(Cipher Block Chaining) с паддингом ANSIX923
    Добавляет IV(Initialization Vector) в начало зашифрованного файла
    :param input_filepath: Путь к исходному файлу, который будет зашифрован
    :param output_filepath: Путь к выходному файлу, куда будут записаны зашифрованные данные
    :param seed_key: Симметричный ключ SEED, используемый для шифрования
    :return: Успешно ли прошло шифрование: да или нет
    """
    print(f"Шифрование файла '{input_filepath}' с использованием SEED...")

    iv = os.urandom(SEED_BLOCK_SIZE)
    cipher = Cipher(algorithms.SEED(seed_key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.ANSIX923(algorithms.SEED.block_size).padder()

    try:
        with open(input_filepath, 'rb') as infile, open(output_filepath, 'wb') as outfile:
            outfile.write(iv)

            while True:
                chunk = infile.read(4096)
                if not chunk:
                    break
                padded_chunk = padder.update(chunk)
                outfile.write(encryptor.update(padded_chunk))

            final_padded_chunk = padder.finalize()
            outfile.write(encryptor.update(final_padded_chunk) + encryptor.finalize())
        print(f"Файл '{input_filepath}' успешно зашифрован в '{output_filepath}'.")
        return True
    except FileNotFoundError:
        print(f"Ошибка: Исходный файл '{input_filepath}' не найден")
        return False
    except Exception as e:
        print(f"Ошибка при шифровании файла: {e}")
        return False


def decrypt_file_seed(input_filepath : str, output_filepath : str, seed_key : bytes)->bool:
    """
    Расшифровывает файл, зашифрованный SEED в режиме CBC(Cipher Block Chaining) с паддингом ANSIX923
    :param input_filepath: Путь к зашифрованному файлу, который нужно расшифровать
    :param output_filepath: Путь к выходному файлу, куда будет записан расшифрованный текст
    :param seed_key: Симметричный ключ SEED, используемый для расшифрования
    :return: Успешно ли прошло расшифровывание: да или нет
    """
    print(f"Расшифрование файла '{input_filepath}' с использованием SEED...")
    try:
        with open(input_filepath, 'rb') as infile, open(output_filepath, 'wb') as outfile:
            iv = infile.read(SEED_BLOCK_SIZE)
            if len(iv) != SEED_BLOCK_SIZE:
                print("Ошибка: Не удалось прочитать вектор инициализации. Файл поврежден или не зашифрован корректно")
                return False

            cipher = Cipher(algorithms.SEED(seed_key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            unpadder = padding.ANSIX923(algorithms.SEED.block_size).unpadder()

            ciphertext = b''
            while True:
                chunk = infile.read(4096)
                if not chunk:
                    break
                ciphertext += chunk

            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
            outfile.write(unpadded_data)
        print(f"Файл '{input_filepath}' успешно расшифрован в '{output_filepath}'")
        return True
    except FileNotFoundError:
        print(f"Ошибка: Зашифрованный файл '{input_filepath}' не найден")
        return False
    except InvalidTag:
        print("Ошибка расшифрования: Неверный ключ или поврежденный файл")
        return False
    except Exception as e:
        print(f"Ошибка при расшифровании файла: {e}")
        return False



def save_bytes_to_file(data : bytes, path : str)->bool:
    """
    Сохраняет зашифрованный ключ файл
    :param data: Зашифрованный ключ
    :param path: Путь к файлу сохранения
    :return: Успешно ли прошло сохранение: Да или Нет
    """
    print(f"Сохранение данных в '{path}'...")
    try:
        with open(path, 'wb') as f:
            f.write(data)
        print("Данные успешно сохранены")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении данных в файл: {e}")
        return False


def load_bytes_from_file(path : str)-> bytes:
    """
    Загружает зашифрованный ключ из файла
    :param path: Путь к файлу
    :return: Зашифрованный ключ
    """
    print(f"Загрузка данных из '{path}'...")
    try:
        with open(path, 'rb') as f:
            data = f.read()
        print("Данные успешно загружены")
        return data
    except FileNotFoundError:
        print(f"Ошибка: Файл '{path}' не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке данных из файла: {e}")
        return None

    