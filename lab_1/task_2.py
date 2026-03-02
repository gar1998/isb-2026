import argparse
import sys

standard_frequencies = [
    (' ', 0.128675), ('О', 0.096456), ('И', 0.075312), ('Е', 0.072292),
    ('А', 0.064841), ('Н', 0.061820), ('Т', 0.061619), ('С', 0.051953),
    ('Р', 0.040677), ('В', 0.039267), ('М', 0.029803), ('Л', 0.029400),
    ('Д', 0.026983), ('Я', 0.026379), ('К', 0.025977), ('П', 0.024768),
    ('З', 0.015908), ('Ы', 0.015707), ('Ь', 0.015103), ('У', 0.013290),
    ('Ч', 0.011679), ('Ж', 0.010673), ('Г', 0.009867), ('Х', 0.008659),
    ('Ф', 0.007249), ('Й', 0.006847), ('Ю', 0.006847), ('Б', 0.006645),
    ('Ц', 0.005034), ('Ш', 0.004229), ('Щ', 0.003625), ('Э', 0.002416),
    ('Ъ', 0.000000)
]


def parse_args() -> argparse.Namespace:
    """
    Разбор аргументов командной строки
    :return: аргументы командной строки
    """

    p = argparse.ArgumentParser()

    p.add_argument("-e",
                   "--encrypted_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\encrypted_text_task_2.txt",
                   help="Путь к зашифрованному тексту")

    p.add_argument("-kp",
                   "--key_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\key_task_2.txt",
                   help="Путь для сохранения значения ключа")

    p.add_argument("-d",
                   "--decrypted_text_path",
                   default="C:\\Users\\Адель\\Desktop\\ОИБ\\Лабораторная работа 1\\"
                           "isb-2026\\lab_1\\decrypted_text_task_2.txt",
                   help="Путь для сохранения дешифрованного текста")

    return p.parse_args()

def clean_encrypted_text(encrypted_text):
    chars = []
    for item in standard_frequencies:
        chars.append(item[0])

    clean_text = []
    for char in encrypted_text:
        if char in chars:
            clean_text.append(char)

    return "".join(clean_text)

def create_file_frequencies(filename, text):
    char_counts = {}
    for char in text:
        char_counts[char] = char_counts.get(char, 0) + 1

    char_frequencies = sorted(char_counts.items(), key=lambda x: x[1], reverse=True)

    with open(filename, 'w', encoding='utf-8') as f:
        for item in char_frequencies:
            f.write(f"\'{item[0]}\' - {round(item[1] / len(text), 6)}")
            f.write("\n")


def main():
    args = parse_args()

    try:
        with open(args.encrypted_text_path, "r") as f:
            encrypted_text = f.read()
    except FileNotFoundError:
        print(f"File path {args.encrypted_text_path} was not found")
        sys.exit(1)

    clean_text = clean_encrypted_text(encrypted_text)

    create_file_frequencies(args.encrypted_frequencies_path, clean_text)





if __name__ == "__main__":
    main()