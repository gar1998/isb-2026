import os
import sys

from PyQt5 import QtWidgets, QtCore, QtGui

from management import load_settings
from symmetric_encryption import (generate_seed_key, encrypt_file_seed, decrypt_file_seed, save_bytes_to_file,
                                  load_bytes_from_file)
from asymmetric_encryption import (generate_rsa_keys, serialize_rsa_private_key,
                                   serialize_rsa_public_key, deserialize_rsa_private_key, deserialize_rsa_public_key,
                                   encrypt_symmetric_key_rsa, decrypt_symmetric_key_rsa)

def generate_keys(settings_paths : dict[str,str])->bool:
    """
    Генерация ключей гибридной системы
    :param settings_paths: Cловарь с путями для текущей операции
    :return: Успешно ли прошла текущая операция: Да или Нет
    """
    print("\nСценарий 1: Генерация ключей гибридной системы")

    seed_key = generate_seed_key()

    private_rsa_key, public_rsa_key = generate_rsa_keys()

    if not serialize_rsa_private_key(private_rsa_key, settings_paths['private_key']):
        return False

    if not serialize_rsa_public_key(public_rsa_key, settings_paths['public_key']):
        return False

    encrypted_seed_key = encrypt_symmetric_key_rsa(seed_key, public_rsa_key)
    if encrypted_seed_key is None:
        return False

    if not save_bytes_to_file(encrypted_seed_key, settings_paths['symmetric_key_encrypted']):
        return False

    print("Сценарий 1 завершен")
    return True


def encrypt_data(settings_paths : dict[str,str]) -> bool:
    """
    Шифрование данных гибридной системой
    :param settings_paths: Cловарь с путями для текущей операции
    :return: Успешно ли прошла текущая операция: Да или Нет
    """
    print("\nСценарий 2: Шифрование данных гибридной системой")

    private_rsa_key = deserialize_rsa_private_key(settings_paths['private_key'])
    if not private_rsa_key:
        print("Невозможно продолжить: закрытый RSA ключ не загружен")
        return False

    encrypted_seed_key = load_bytes_from_file(settings_paths['symmetric_key_encrypted'])
    if not encrypted_seed_key:
        print("Невозможно продолжить: зашифрованный симметричный ключ не загружен")
        return False

    seed_key = decrypt_symmetric_key_rsa(encrypted_seed_key, private_rsa_key)
    if seed_key is None:
        print("Невозможно продолжить: симметричный ключ не расшифрован")
        return False

    if not encrypt_file_seed(settings_paths['initial_file'], settings_paths['encrypted_file'], seed_key):
        return False

    print("Сценарий 2 завершен")
    return True


def decrypt_data(settings_paths : dict[str,str]) -> bool:
    """
    Дешифрование данных гибридной системой
    :param settings_paths: Cловарь с путями для текущей операции
    :return: Успешно ли прошла текущая операция: Да или Нет
    """
    print("\nСценарий 3: Дешифрование данных гибридной системой")

    private_rsa_key = deserialize_rsa_private_key(settings_paths['private_key'])
    if not private_rsa_key:
        print("Невозможно продолжить: закрытый RSA ключ не загружен")
        return False

    encrypted_seed_key = load_bytes_from_file(settings_paths['symmetric_key_encrypted'])
    if not encrypted_seed_key:
        print("Невозможно продолжить: зашифрованный симметричный ключ не загружен.")
        return False

    seed_key = decrypt_symmetric_key_rsa(encrypted_seed_key, private_rsa_key)
    if seed_key is None:
        print("Невозможно продолжить: симметричный ключ не расшифрован.")
        return False

    if not decrypt_file_seed(settings_paths['encrypted_file'], settings_paths['decrypted_file'], seed_key):
        return False

    print("Сценарий 3 завершен")
    return True



class Stream(QtCore.QObject):
    """Custom stream to redirect stdout to a QTextEdit widget."""
    newText = QtCore.pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QtWidgets.QApplication.processEvents()

    def flush(self):
        pass


class HybridCryptoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.init_ui()
        self.load_app_settings()
        self.create_initial_file_if_not_exists()

        self.original_stdout = sys.stdout
        sys.stdout = Stream(newText=self.on_update_log)

    def init_ui(self):
        self.setWindowTitle("Гибридная криптосистема (SEED + RSA)")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QtWidgets.QVBoxLayout(central_widget)

        self.tabs = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tabs)

        self.create_generation_tab()
        self.create_encryption_tab()
        self.create_decryption_tab()

        self.log_text_edit = QtWidgets.QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(QtGui.QFont("Consolas", 9))
        main_layout.addWidget(QtWidgets.QLabel("Лог выполнения:"))
        main_layout.addWidget(self.log_text_edit)

        self.statusBar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Приложение готово.")

    def create_generation_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(tab)
        self.tabs.addTab(tab, "1. Генерация ключей")

        self.gen_sym_key_enc_path = QtWidgets.QLineEdit()
        self.gen_pub_key_path = QtWidgets.QLineEdit()
        self.gen_priv_key_path = QtWidgets.QLineEdit()

        layout.addRow("Зашифрованный симметричный ключ (.txt):",
                      self.create_file_selector(self.gen_sym_key_enc_path, save=True,
                                                filter="Text files (*.txt);;All files (*.*)"))
        layout.addRow("Открытый RSA ключ (.pem):", self.create_file_selector(self.gen_pub_key_path, save=True,
                                                                             filter="PEM files (*.pem);;All files (*.*)"))
        layout.addRow("Закрытый RSA ключ (.pem):", self.create_file_selector(self.gen_priv_key_path, save=True,
                                                                             filter="PEM files (*.pem);;All files (*.*)"))

        generate_button = QtWidgets.QPushButton("Сгенерировать ключи")
        generate_button.clicked.connect(self.run_scenario_1)
        layout.addRow(generate_button)

    def create_encryption_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(tab)
        self.tabs.addTab(tab, "2. Шифрование данных")

        self.enc_initial_file_path = QtWidgets.QLineEdit()
        self.enc_private_key_path = QtWidgets.QLineEdit()
        self.enc_sym_key_enc_path = QtWidgets.QLineEdit()
        self.enc_encrypted_file_path = QtWidgets.QLineEdit()

        layout.addRow("Исходный файл (.txt):", self.create_file_selector(self.enc_initial_file_path, save=False,
                                                                         filter="Text files (*.txt);;All files (*.*)"))
        layout.addRow("Закрытый RSA ключ (.pem):", self.create_file_selector(self.enc_private_key_path, save=False,
                                                                             filter="PEM files (*.pem);;All files (*.*)"))
        layout.addRow("Зашифрованный симметричный ключ (.txt):",
                      self.create_file_selector(self.enc_sym_key_enc_path, save=False,
                                                filter="Text files (*.txt);;All files (*.*)"))
        layout.addRow("Выходной зашифрованный файл (.txt):",
                      self.create_file_selector(self.enc_encrypted_file_path, save=True,
                                                filter="Text files (*.txt);;All files (*.*)"))

        encrypt_button = QtWidgets.QPushButton("Зашифровать данные")
        encrypt_button.clicked.connect(self.run_scenario_2)
        layout.addRow(encrypt_button)

    def create_decryption_tab(self):
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(tab)
        self.tabs.addTab(tab, "3. Дешифрование данных")

        self.dec_encrypted_file_path = QtWidgets.QLineEdit()
        self.dec_private_key_path = QtWidgets.QLineEdit()
        self.dec_sym_key_enc_path = QtWidgets.QLineEdit()
        self.dec_decrypted_file_path = QtWidgets.QLineEdit()

        layout.addRow("Входной зашифрованный файл (.txt):",
                      self.create_file_selector(self.dec_encrypted_file_path, save=False,
                                                filter="Text files (*.txt);;All files (*.*)"))
        layout.addRow("Закрытый RSA ключ (.pem):", self.create_file_selector(self.dec_private_key_path, save=False,
                                                                             filter="PEM files (*.pem);;All files (*.*)"))
        layout.addRow("Зашифрованный симметричный ключ (.txt):",
                      self.create_file_selector(self.dec_sym_key_enc_path, save=False,
                                                filter="Text files (*.txt);;All files (*.*)"))
        layout.addRow("Выходной расшифрованный файл (.txt):",
                      self.create_file_selector(self.dec_decrypted_file_path, save=True,
                                                filter="Text files (*.txt);;All files (*.*)"))

        decrypt_button = QtWidgets.QPushButton("Расшифровать данные")
        decrypt_button.clicked.connect(self.run_scenario_3)
        layout.addRow(decrypt_button)

    def create_file_selector(self, line_edit, save=False, filter="All files (*.*)"):
        """Helper to create a QLineEdit with a browse button."""
        widget = QtWidgets.QWidget()
        h_layout = QtWidgets.QHBoxLayout(widget)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addWidget(line_edit)
        browse_button = QtWidgets.QPushButton("Обзор...")
        browse_button.clicked.connect(lambda: self.browse_file(line_edit, save, filter))
        h_layout.addWidget(browse_button)
        return widget

    def browse_file(self, line_edit, save, filter):
        """Opens a file dialog and sets the selected path to the line edit."""
        current_path = line_edit.text()
        if save:
            filepath, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить файл", current_path, filter)
        else:
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", current_path, filter)

        if filepath:
            line_edit.setText(filepath)

    def load_app_settings(self):
        """Loads settings from JSON and populates GUI fields."""
        settings, error_msg = load_settings()
        if error_msg:
            QtWidgets.QMessageBox.critical(self, "Ошибка загрузки настроек", error_msg)
            self.statusBar.showMessage("Ошибка: Не удалось загрузить настройки.")
            self.tabs.setEnabled(False)
            return

        self.settings = settings
        self.statusBar.showMessage("Настройки успешно загружены.")

        self.gen_sym_key_enc_path.setText(self.settings.get('symmetric_key_encrypted', ''))
        self.gen_pub_key_path.setText(self.settings.get('public_key', ''))
        self.gen_priv_key_path.setText(self.settings.get('private_key', ''))

        self.enc_initial_file_path.setText(self.settings.get('initial_file', ''))
        self.enc_private_key_path.setText(self.settings.get('private_key', ''))
        self.enc_sym_key_enc_path.setText(self.settings.get('symmetric_key_encrypted', ''))
        self.enc_encrypted_file_path.setText(self.settings.get('encrypted_file', ''))

        self.dec_encrypted_file_path.setText(self.settings.get('encrypted_file', ''))
        self.dec_private_key_path.setText(self.settings.get('private_key', ''))
        self.dec_sym_key_enc_path.setText(self.settings.get('symmetric_key_encrypted', ''))
        self.dec_decrypted_file_path.setText(self.settings.get('decrypted_file', ''))

    def create_initial_file_if_not_exists(self):
        """Создает фиктивный исходный файл для тестирования, если он не существует."""
        initial_file_path = self.settings.get('initial_file')
        if not initial_file_path:
            print("Путь к исходному файлу не указан в настройках.")
            return

        if not os.path.exists(initial_file_path):
            dirname = os.path.dirname(initial_file_path)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)
            try:
                with open(initial_file_path, 'w', encoding='utf-8') as f:
                    f.write("Это тестовый файл для демонстрации работы гибридной криптосистемы.\n")
                    f.write("Он должен быть достаточно объемным, чтобы показать преимущества блочного шифра.\n")
                    f.write("Повторяем текст много раз для объема:\n")
                    for i in range(100):
                        f.write(
                            f"Строка {i + 1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n")
                print(f"Создан тестовый файл '{initial_file_path}' для шифрования.")
            except Exception as e:
                print(f"Ошибка при создании тестового файла '{initial_file_path}': {e}")

    @QtCore.pyqtSlot(str)
    def on_update_log(self, text):
        """Слот для добавления текста в окно лога."""
        cursor = self.log_text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.log_text_edit.setTextCursor(cursor)
        self.log_text_edit.ensureCursorVisible()

    def run_scenario_1(self):
        self.log_text_edit.clear()
        self.statusBar.showMessage("Выполняется сценарий 1: Генерация ключей...")

        current_paths = {
            'symmetric_key_encrypted': self.gen_sym_key_enc_path.text(),
            'public_key': self.gen_pub_key_path.text(),
            'private_key': self.gen_priv_key_path.text(),
        }

        for key, path in current_paths.items():
            if not path:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Путь для '{key}' не может быть пустым.")
                self.statusBar.showMessage("Сценарий 1 завершен с ошибкой.")
                return

        if generate_keys(current_paths):
            self.statusBar.showMessage("Сценарий 1 завершен успешно.")
            QtWidgets.QMessageBox.information(self, "Успех", "Ключи успешно сгенерированы!")
        else:
            self.statusBar.showMessage("Сценарий 1 завершен с ошибкой.")
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Произошла ошибка при генерации ключей. См. лог.")

    def run_scenario_2(self):
        self.log_text_edit.clear()
        self.statusBar.showMessage("Выполняется сценарий 2: Шифрование данных...")

        current_paths = {
            'initial_file': self.enc_initial_file_path.text(),
            'private_key': self.enc_private_key_path.text(),
            'symmetric_key_encrypted': self.enc_sym_key_enc_path.text(),
            'encrypted_file': self.enc_encrypted_file_path.text(),
        }

        for key, path in current_paths.items():
            if not path:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Путь для '{key}' не может быть пустым.")
                self.statusBar.showMessage("Сценарий 2 завершен с ошибкой.")
                return

        if encrypt_data(current_paths):
            self.statusBar.showMessage("Сценарий 2 завершен успешно.")
            QtWidgets.QMessageBox.information(self, "Успех", "Данные успешно зашифрованы!")
        else:
            self.statusBar.showMessage("Сценарий 2 завершен с ошибкой.")
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Произошла ошибка при шифровании данных. См. лог.")

    def run_scenario_3(self):
        self.log_text_edit.clear()
        self.statusBar.showMessage("Выполняется сценарий 3: Дешифрование данных...")

        current_paths = {
            'encrypted_file': self.dec_encrypted_file_path.text(),
            'private_key': self.dec_private_key_path.text(),
            'symmetric_key_encrypted': self.dec_sym_key_enc_path.text(),
            'decrypted_file': self.dec_decrypted_file_path.text(),
        }

        for key, path in current_paths.items():
            if not path:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Путь для '{key}' не может быть пустым.")
                self.statusBar.showMessage("Сценарий 3 завершен с ошибкой.")
                return

        if decrypt_data(current_paths):
            self.statusBar.showMessage("Сценарий 3 завершен успешно.")
            QtWidgets.QMessageBox.information(self, "Успех", "Данные успешно расшифрованы!")
        else:
            self.statusBar.showMessage("Сценарий 3 завершен с ошибкой.")
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Произошла ошибка при дешифровании данных. См. лог.")

    def closeEvent(self, event):
        """Восстанавливаем stdout при закрытии приложения."""
        sys.stdout = self.original_stdout
        super().closeEvent(event)