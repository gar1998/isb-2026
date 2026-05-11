import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives import serialization
from constants import RSA_KEY_SIZE

from symmetric_encryption import generate_seed_key

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


def encrypt_symmetric_key_rsa(symmetric_key : bytes, public_key : rsa.RSAPublicKey)->bytes:
    """
    Шифрует симметричный ключ с использованием открытого RSA ключа с паддингом OAEP
    :param symmetric_key: Симметричный ключ, который будет зашифрован RSA-открытым ключом
    :param public_key: Открытый RSA ключ
    :return: Зашифрованный симметричный ключ
    """
    print("Шифрование симметричного ключа RSA открытым ключом...")
    try:
        encrypted_key = public_key.encrypt(
            symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ зашифрован RSA")
        return encrypted_key
    except Exception as e:
        print(f"Ошибка при шифровании симметричного ключа: {e}")
        return None


def decrypt_symmetric_key_rsa(encrypted_symmetric_key : bytes, private_key : rsa.RSAPrivateKey)->bytes:
    """
    Расшифровывает RSA-зашифрованный симметричный ключ с использованием закрытого RSA ключа с паддингом OAEP
    :param encrypted_symmetric_key: RSA-зашифрованный симметричный ключ
    :param private_key: Закрытый RSA ключ
    :return: Расшифрованный симметричный ключ
    """
    print("Расшифрование симметричного ключа RSA закрытым ключом...")
    try:
        decrypted_key = private_key.decrypt(
            encrypted_symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("Симметричный ключ расшифрован RSA")
        return decrypted_key
    except ValueError:
        print("Ошибка расшифрования симметричного ключа: Неверный закрытый ключ или поврежденные данные")
        return None
    except Exception as e:
        print(f"Ошибка при расшифровании симметричного ключа: {e}")
        return None
