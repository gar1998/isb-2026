import math
import os
from parameters import SEQUENCE_CPP, SEQUENCE_JAVA, OUTPUT_FILE
from scipy.special import erfc, gammaincc
import sys


def frequency_test(binary_sequence: str) -> float:
    """
    Частотный побитовый тест
    :param binary_sequence:
    :return: вычисленное P-значение
    """
    sequence_length = len(binary_sequence)
    accumulated_sum = 0

    for bit in binary_sequence:
        if bit == '1':
            accumulated_sum = accumulated_sum + 1
        else:
            accumulated_sum = accumulated_sum - 1

    observed_statistic = abs(accumulated_sum) / math.sqrt(sequence_length)

    p_value = erfc(observed_statistic / math.sqrt(2))

    return p_value


def runs_test(binary_sequence: str) -> float:
    """
    Тест на одинаковые подряд идущие биты
    :param binary_sequence: двоичная последовательность
    :return: вычисленное P-значение
    """
    sequence_length = len(binary_sequence)

    ones_count = 0
    for bit in binary_sequence:
        if bit == '1':
            ones_count = ones_count + 1

    proportion_of_ones = ones_count / sequence_length

    standard_deviation = 2 / math.sqrt(sequence_length)
    if abs(proportion_of_ones - 0.5) >= standard_deviation:
        return 0

    actual_runs = 1
    for index in range(sequence_length - 1):
        if binary_sequence[index] != binary_sequence[index + 1]:
            actual_runs = actual_runs + 1

    numerator = abs(actual_runs - 2 * sequence_length * proportion_of_ones * (1 - proportion_of_ones))
    denominator = (2 * math.sqrt(2 * sequence_length) * proportion_of_ones * (1 - proportion_of_ones))

    p_value = erfc(numerator / denominator)

    return p_value


def longest_run_of_ones_test(binary_sequence: str) -> float:
    """
    Тест на самую длинную последовательность единиц в блоке
    :param binary_sequence: двоичная последовательность
    :return: вычисленное P-значение
    """
    block_size = 8
    number_of_blocks = 16

    theoretical_probabilities = [0.2148, 0.3672, 0.2305, 0.1875]

    v_frequencies = [0, 0, 0, 0]

    for i in range(number_of_blocks):
        start_index = i * block_size
        end_index = (i + 1) * block_size
        block = binary_sequence[start_index:end_index]

        max_run = 0
        current_run = 0
        for bit in block:
            if bit == '1':
                current_run = current_run + 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0

        if max_run <= 1:
            v_frequencies[0] = v_frequencies[0] + 1
        elif max_run == 2:
            v_frequencies[1] = v_frequencies[1] + 1
        elif max_run == 3:
            v_frequencies[2] = v_frequencies[2] + 1
        else:
            v_frequencies[3] = v_frequencies[3] + 1

    chi_square_statistic = 0
    for j in range(4):
        expected_value = number_of_blocks * theoretical_probabilities[j]
        difference = (v_frequencies[j] - expected_value) ** 2
        chi_square_statistic = chi_square_statistic + (difference / expected_value)

    p_value = gammaincc(3 / 2, chi_square_statistic / 2)

    return p_value


def perform_analysis(file_path: str, report_file: str) -> None:
    """
    Функция для считывания файла и вывода результатов тестирования
    :param file_path: путь к файлу с двоичной последовательностью
    :param report_file: путь к итоговому файлу
    """
    if not os.path.exists(file_path):
        print(f"File path {file_path} was not found")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sequence = file.read().strip()
    except FileNotFoundError:
        print(f"File path {file_path} was not found")
        sys.exit(1)

    p_freq = frequency_test(sequence)
    p_runs = runs_test(sequence)
    p_longest = longest_run_of_ones_test(sequence)

    test_results = [
        ("Частотный тест", p_freq),
        ("Тест на серии", p_runs),
        ("Длинная серия единиц", p_longest)
    ]

    try:
        with open(report_file, 'a', encoding='utf-8') as report:

            report.write(f"\nАнализ файла: {file_path}\n")
            report.write(f"Длина последовательности: {len(sequence)} бит\n")

            for test_name, p_val in test_results:
                if p_val >= 0.01:
                    conclusion = "ПРОЙДЕН"
                else:
                    conclusion = "НЕ ПРОЙДЕН"

                output_line = f"{test_name:25} | P-value: {p_val:.6f} | Результат: {conclusion}"

                report.write(output_line + "\n")
    except FileNotFoundError:
        print(f"File path {report_file} was not found")
        sys.exit(1)

if __name__ == "__main__":
    perform_analysis(SEQUENCE_CPP, OUTPUT_FILE)
    perform_analysis(SEQUENCE_JAVA, OUTPUT_FILE)