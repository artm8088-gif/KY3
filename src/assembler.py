"""Модуль ассемблера для перевода текста в промежуточное представление."""

import re
from typing import Any


class AssemblerError(Exception):
    """Ошибка ассемблирования."""


class Assembler:
    """Класс для перевода текста ассемблера в промежуточное представление."""

    # Карта команд: мнемоника -> opcode (A)
    OPCODES = {
        "LOAD": 1,  # Загрузка константы (A=1)
        "LOADM": 12,  # Чтение из памяти со смещением (A=12)
        "STORE": 0,  # Запись в память (A=0)
        "ADD": 9,  # Сложение (A=9)
    }

    def __init__(self) -> None:
        """Инициализация ассемблера."""
        self.instructions: list[dict[str, Any]] = []

    def parse_line(self, line: str) -> dict[str, Any]:
        """Разбирает одну строку и возвращает словарь (IR)."""
        # Убираем комментарии и пробелы
        line = line.split(";")[0].strip()
        if not line:
            return {}

        # Разделяем на мнемонику и аргументы
        parts = re.split(r"[\s,]+", line)
        mnemonic = parts[0].upper()

        if mnemonic not in self.OPCODES:
            raise AssemblerError(f"Неизвестная команда: {mnemonic}")

        opcode = self.OPCODES[mnemonic]
        instruction: dict[str, Any] = {"mnemonic": mnemonic, "A": opcode, "B": 0}

        if mnemonic == "LOAD":
            if len(parts) < 2:
                raise AssemblerError(f"Команда {mnemonic} требует аргумент")
            try:
                instruction["B"] = int(parts[1])
            except ValueError:
                raise AssemblerError(f"Ожидалось число, получено: {parts[1]}")

        elif mnemonic == "LOADM":
            if len(parts) < 2:
                raise AssemblerError(f"Команда {mnemonic} требует аргумент (смещение)")
            try:
                instruction["B"] = int(parts[1])
            except ValueError:
                raise AssemblerError(f"Ожидалось число, получено: {parts[1]}")

        return instruction

    def assemble(self, source_code: str) -> list[dict[str, Any]]:
        """Переводит весь текст программы в IR."""
        self.instructions = []
        for line_num, line in enumerate(source_code.splitlines(), 1):
            try:
                ir = self.parse_line(line)
                if ir:
                    self.instructions.append(ir)
            except AssemblerError as e:
                raise AssemblerError(f"Строка {line_num}: {e}")
        return self.instructions
