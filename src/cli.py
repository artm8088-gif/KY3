"""Модуль CLI для ассемблера."""

import argparse
from typing import Any

from src.assembler import Assembler


def print_ir(instructions: list[dict[str, Any]]) -> None:
    """Выводит промежуточное представление в формате тестов."""
    print("Промежуточное представление (IR):")
    print("=" * 40)
    for idx, instr in enumerate(instructions):
        print(f"Команда {idx + 1}: {instr['mnemonic']}")
        print(f"  Поле A (Opcode): {instr['A']}")
        print(f"  Поле B (Operand): {instr['B']}")
        print("-" * 40)


def main() -> None:
    """Точка входа CLI."""
    parser = argparse.ArgumentParser(description="Ассемблер УВМ (Этап 1)")
    parser.add_argument("-i", "--input", required=True, help="Путь к исходному файлу")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help="Путь к бинарному файлу (заглушка на этапе 1)",
    )
    parser.add_argument("-t", "--test", action="store_true", help="Режим тестирования")

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

    if args.test:
        print_ir(ir)
    else:
        print(f"Успешно прочитано {len(ir)} команд. (Бинарная генерация на Этапе 2)")
