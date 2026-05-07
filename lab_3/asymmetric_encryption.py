import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from constants import RSA_KEY_SIZE



def generate_rsa_keys()->tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Генерирует пару RSA ключей (открытый и закрытый)
    :return: Пара RSA ключей (открытый и закрытый)
    """
    print("Генерация RSA ключей (закрытого и открытого)...")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=RSA_KEY_SIZE
    )
    public_key = private_key.public_key()

    print("RSA ключи сгенерированы.")
    return private_key, public_key


def serialize_rsa_private_key(private_key : rsa.RSAPrivateKey, path : str)->bool:
    """
    Сериализует закрытый RSA ключ в PEM-файл
    :param private_key: Закрытый RSA ключ
    :param path: Путь для закрытого RSA ключа
    :return: Успешно ли прошла сериализация: да или нет
    """
    print(f"Сериализация закрытого RSA ключа в '{path}'...")

    try:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(path, 'wb') as f:
            f.write(pem)
        print("Закрытый RSA ключ сериализован")
        return True
    except Exception as e:
        print(f"Ошибка при сериализации закрытого RSA ключа: {e}")
        return False


def serialize_rsa_public_key(public_key : rsa.RSAPublicKey, path : str)->bool:
    """
    Сериализует открытый RSA ключ в PEM-файл
    :param public_key: Открытый RSA ключ
    :param path: Путь для открытого RSA ключа
    :return: Успешно ли прошла сериализация: да или нет
    """
    print(f"Сериализация открытого RSA ключа в '{path}'...")
    try:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        with open(path, 'wb') as f:
            f.write(pem)
        print("Открытый RSA ключ сериализован")
        return True
    except Exception as e:
        print(f"Ошибка при сериализации открытого RSA ключа: {e}")
        return False


def deserialize_rsa_private_key(path : str)->rsa.RSAPrivateKey:
    """
    Десериализует закрытый RSA ключ из PEM-файла
    :param path: Путь к PEM-файлу закрытого RSA ключа
    :return: Закрытый RSA ключ
    """
    print(f"Десериализация закрытого RSA ключа из '{path}'...")
    try:
        with open(path, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        print("Закрытый RSA ключ десериализован")
        return private_key
    except FileNotFoundError:
        print(f"Ошибка: Файл закрытого RSA ключа '{path}' не найден")
        return None
    except ValueError:
        print(f"Ошибка: Неверный формат файла закрытого RSA ключа '{path}'")
        return None
    except Exception as e:
        print(f"Ошибка при десериализации закрытого RSA ключа: {e}")
        return None


def deserialize_rsa_public_key(path : str)->rsa.RSAPublicKey:
    """
    Десериализует открытый RSA ключ из PEM-файла
    :param path: Путь к PEM-файлу открытого RSA ключа
    :return: Открытый RSA ключ
    """
    print(f"Десериализация открытого RSA ключа из '{path}'...")
    try:
        with open(path, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        print("Открытый RSA ключ десериализован")
        return public_key
    except FileNotFoundError:
        print(f"Ошибка: Файл открытого RSA ключа '{path}' не найден")
        return None
    except ValueError:
        print(f"Ошибка: Неверный формат файла открытого RSA ключа '{path}'")
        return None
    except Exception as e:
        print(f"Ошибка при десериализации открытого RSA ключа: {e}")
        return None


if __name__ == "__main__":
    private_key_path = "test_private.pem"
    public_key_path = "test_public.pem"

    private_rsa_key, public_rsa_key = generate_rsa_keys()
    if private_rsa_key and public_rsa_key:
        print("Генерация RSA ключей: УСПЕШНО")
    else:
        print("Генерация RSA ключей: ПРОВАЛ")

    if serialize_rsa_private_key(private_rsa_key, private_key_path) and \
            serialize_rsa_public_key(public_rsa_key, public_key_path):
        print("Сериализация RSA ключей: УСПЕШНО")
    else:
        print("Сериализация RSA ключей: ПРОВАЛ")

    deserialized_private_key = deserialize_rsa_private_key(private_key_path)
    deserialized_public_key = deserialize_rsa_public_key(public_key_path)

    if deserialized_private_key and deserialized_public_key:
        print("Десериализация RSA ключей: УСПЕШНО")

        if deserialized_private_key and deserialized_public_key:
            print("Проверка десериализованных ключей: УСПЕШНО")
        else:
            print("Проверка десериализованных ключей: ПРОВАЛ")
    else:
        print("Десериализация RSA ключей: ПРОВАЛ")

    for f in [private_key_path, public_key_path]:
        if os.path.exists(f):
            os.remove(f)
            print(f"Удален {f}")