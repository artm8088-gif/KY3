"""Модуль ассемблера для перевода текста в промежуточное представление (IR).

Этот модуль читает текст программы на языке ассемблера и преобразует его
в список словарей, где каждый словарь описывает одну команду УВМ.
"""

import re
from typing import Any


class AssemblerError(Exception):
    """Исключение, возникающее при синтаксических ошибках в тексте ассемблера.

    Например, если команда неизвестна или аргумент не является числом.
    """


class Assembler:
    """Класс для разбора текста ассемблера в промежуточное представление.

    Поддерживаемые команды (Вариант №2):
        LOAD  <число>  (A=1, B=константа)
        LOADM <число>  (A=12, B=смещение)
        STORE          (A=0)
        ADD            (A=9)
    """

    OPCODES = {
        "LOAD": 1,
        "LOADM": 12,
        "STORE": 0,
        "ADD": 9,
    }

    MIN_PARTS_WITH_ARG = 2

    def __init__(self) -> None:
        """Инициализация ассемблера.

        Создает пустой список для хранения разобранных инструкций.
        """
        self.instructions: list[dict[str, Any]] = []

    def parse_line(self, line: str) -> dict[str, Any]:
        """Разбирает одну строку текста и возвращает словарь (IR).

        Строка очищается от комментариев (все, что после ';').
        Если строка пустая — возвращается пустой словарь.
        Команда разбивается на мнемонику и аргументы
        с помощью регулярного выражения.

        Аргументы:
            line (str): Одна строка исходного кода.

        Возвращает:
            Dict[str, Any]: Словарь с полями 'mnemonic', 'A', 'B'.
                            Пустой словарь, если строка не содержит команды.

        Исключения:
            AssemblerError: Если команда неизвестна или аргумент не число.
        """
        line = line.split(";", maxsplit=1)[0].strip()
        if not line:
            return {}

        parts = re.split(r"[\s,]+", line)
        mnemonic = parts[0].upper()

        if mnemonic not in self.OPCODES:
            raise AssemblerError(f"Неизвестная команда: {mnemonic}")

        opcode = self.OPCODES[mnemonic]
        instruction: dict[str, Any] = {
            "mnemonic": mnemonic,
            "A": opcode,
            "B": 0,
        }

        if mnemonic in ("LOAD", "LOADM"):
            if len(parts) < self.MIN_PARTS_WITH_ARG:
                raise AssemblerError(f"Команда {mnemonic} требует аргумент")
            try:
                instruction["B"] = int(parts[1])
            except ValueError:
                raise AssemblerError(f"Ожидалось число, получено: {parts[1]}")

        return instruction

    def assemble(self, source_code: str) -> list[dict[str, Any]]:
        """Переводит весь текст программы в список инструкций (IR).

        Проходит по каждой строке исходного кода, вызывает parse_line,
        и собирает непустые результаты в общий список.

        Аргументы:
            source_code (str): Полный текст программы на ассемблере.

        Возвращает:
            List[Dict[str, Any]]: Список словарей с инструкциями.

        Исключения:
            AssemblerError: Если в какой-то строке найдена ошибка
                            (с указанием номера строки).
        """
        self.instructions = []
        for line_num, line in enumerate(source_code.splitlines(), 1):
            try:
                ir = self.parse_line(line)
                if ir:
                    self.instructions.append(ir)
            except AssemblerError as e:
                raise AssemblerError(f"Строка {line_num}: {e}")
        return self.instructions
