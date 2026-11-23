"""Модуль командной строки для ассемблера УВМ (Этап 2).

Этот модуль отвечает за:
1. Разбор аргументов командной строки (-i, -o, -t).
2. Чтение исходного файла ассемблера.
3. Запуск процесса ассемблирования и кодирования.
4. Запись бинарного файла.
5. Вывод статистики и байтов в режиме тестирования.
"""

import argparse

from src.assembler import Assembler
from src.encoder import Encoder


def print_bytes(bytecode: bytes) -> None:
    """Выводит машинный код в шестнадцатеричном формате, как в тестах.

    Пример вывода: "0x01, 0x08, 0x00, 0x00, 0x00"

    Аргументы:
        bytecode (bytes): Строка байтов для вывода.
    """
    print("Машинный код (hex):")
    hex_str = ", ".join(f"0x{byte:02X}" for byte in bytecode)
    print(hex_str)
    print("=" * 40)


def main() -> None:
    """Главная функция программы.

    Управляет всем процессом: от чтения аргументов до записи файла.
    Использует argparse для разбора флагов -i, -o, -t.
    """
    parser = argparse.ArgumentParser(description="Ассемблер УВМ (Этап 2)")
    parser.add_argument(
        "-i",
        "--input",
        required=True,
        help="Путь к исходному файлу с текстом программы",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Путь к бинарному файлу-результату",
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Режим тестирования: вывести байты на экран",
    )

    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл {args.input} не найден.")
        return

    asm = Assembler()
    try:
        ir = asm.assemble(source)
    except Exception as e:
        print(f"Ошибка ассемблирования: {e}")
        return

    encoder = Encoder()
    try:
        bytecode = encoder.encode(ir)
    except Exception as e:
        print(f"Ошибка кодирования: {e}")
        return

    with open(args.output, "wb") as f:
        f.write(bytecode)

    print(f"Успешно ассемблировано команд: {len(ir)}")
    print(f"Размер выходного файла: {len(bytecode)} байт")

    if args.test:
        print_bytes(bytecode)
