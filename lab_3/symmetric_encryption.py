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

    
if __name__ == "__main__":
    input_filepath = "test_input.txt"
    encrypted_filepath = "test_encrypted.bin"
    decrypted_filepath = "test_decrypted.txt"
    original_content = b"The task of the organization, especially the further development of various forms of activity, is an interesting experiment to test the personnel training system that meets the urgent needs. Higher-level considerations, as well as a new organizational model, contribute to the preparation and implementation of new proposals. The importance of these issues is so obvious that the implementation of the planned development plan ensures the relevance of comprehensively balanced innovations. On the other hand, the constant information and technical support of our activities plays an important role in shaping the key components of the planned upgrade. Considerations of the highest order, as well as consultation with IT professionals, directly depend on the further directions of the project development. Practical experience shows that the new model of organizational activity makes it possible to complete the most important tasks for developing new proposals. Higher-order considerations, as well as consultation with IT professionals, require determining and clarifying the economic feasibility of the decisions being made. Higher-level considerations, as well as constant information and technical support for our activities, contribute to increasing the relevance of the development model. However, one should not forget that the beginning of daily work on the formation of a position allows us to assess the importance of a personnel training system that meets urgent needs. Everyday practice shows that the new model of organizational activity contributes to increasing the relevance of the development model. On the other hand, consulting with IT professionals directly depends on the key components of the planned upgrade. Practical experience shows that the further development of various forms of activity requires us to systematically analyze the appropriate activation conditions. Higher-order considerations, as well as the innovative path we have chosen, allow us to complete the most important tasks for developing new proposals. However, one should not forget that the course towards a socially oriented national project makes it possible to assess the importance of the economic feasibility of the decisions taken." * 10

    with open(input_filepath, 'wb') as f:
        f.write(original_content)
    print(f"Создан тестовый входной файл: {input_filepath}")

    seed_key = generate_seed_key()
    print(f"Сгенерирован SEED ключ: {seed_key.hex()}")

    if encrypt_file_seed(input_filepath, encrypted_filepath, seed_key):
        print("Тест шифрования: УСПЕШНО")
    else:
        print("Тест шифрования: ПРОВАЛ.")

    if decrypt_file_seed(encrypted_filepath, decrypted_filepath, seed_key):
        print("Тест дешифрования: УСПЕШНО")
    else:
        print("Тест дешифрования: ПРОВАЛ.")

    try:
        with open(decrypted_filepath, 'rb') as f:
            decrypted_content = f.read()
        if original_content == decrypted_content:
            print("Проверка содержимого: УСПЕШНО")
        else:
            print("Проверка содержимого: ПРОВАЛ")
    except FileNotFoundError:
        print("Проверка содержимого: ПРОВАЛ")

    for f in [input_filepath, encrypted_filepath, decrypted_filepath]:
        if os.path.exists(f):
            os.remove(f)
            print(f"Удален {f}")