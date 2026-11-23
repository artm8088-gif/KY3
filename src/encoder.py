"""Модуль кодирования промежуточного представления в машинный код."""

from typing import Any


class EncoderError(Exception):
    """Исключение, возникающее при ошибках кодирования."""


class Encoder:
    """Класс для перевода промежуточного представления (IR) в байты.

    Атрибуты класса:
        COMMAND_SIZE_BYTES (int): Размер одной команды УВМ в байтах.
        BITS_PER_BYTE (int): Количество бит в одном байте.
        BYTE_MASK (int): Маска для извлечения одного байта.
        OPCODE_BITS (int): Количество бит, отведенных под поле A (Opcode).
        MAX_LOAD_CONST (int): Максимальное значение константы для LOAD.
        MAX_LOADM_OFFSET (int): Максимальное смещение для LOADM.
    """

    COMMAND_SIZE_BYTES = 5
    BITS_PER_BYTE = 8
    BYTE_MASK = 0xFF
    OPCODE_BITS = 4
    MAX_LOAD_CONST = 0xFFFFFFFF
    MAX_LOADM_OFFSET = 0x3FFF

    def __init__(self) -> None:
        """Инициализация кодировщика.

        Создает пустой буфер для хранения машинного кода.
        """
        self.bytecode: bytearray = bytearray()

    def encode_instruction(self, instr: dict[str, Any]) -> None:
        """Кодирует одну инструкцию в 5 байт и добавляет их в буфер.

        В зависимости от мнемоники команды, поля A и B упаковываются
        в одно 40-битное целое число с помощью побитовых сдвигов.
        Затем это число разбивается на 5 байт (Little-Endian).

        Аргументы:
            instr (Dict[str, Any]): Словарь с ключами 'mnemonic', 'A', 'B'.

        Исключения:
            EncoderError: Если значение B выходит за допустимые пределы
                          или команда неизвестна.
        """
        mnemonic = instr["mnemonic"]
        a = instr["A"]
        b = instr["B"]

        if mnemonic == "LOAD":
            if not (0 <= b <= self.MAX_LOAD_CONST):
                raise EncoderError(
                    f"Константа {b} не влезает в 32 бита "
                    f"(максимум {self.MAX_LOAD_CONST})"
                )
            command_int = a | (b << self.OPCODE_BITS)

        elif mnemonic == "LOADM":
            if not (0 <= b <= self.MAX_LOADM_OFFSET):
                raise EncoderError(
                    f"Смещение {b} не влезает в 14 бит "
                    f"(максимум {self.MAX_LOADM_OFFSET})"
                )
            command_int = a | (b << self.OPCODE_BITS)

        elif mnemonic in ("STORE", "ADD"):
            command_int = a

        else:
            raise EncoderError(
                f"Неизвестная команда для кодирования: {mnemonic}"
            )

        for _ in range(self.COMMAND_SIZE_BYTES):
            self.bytecode.append(command_int & self.BYTE_MASK)
            command_int >>= self.BITS_PER_BYTE

    def encode(self, instructions: list[dict[str, Any]]) -> bytes:
        """Кодирует весь список инструкций в единую последовательность байтов.

        Аргументы:
            instructions (List[Dict[str, Any]]): Список словарей (IR).

        Возвращает:
            bytes: Итоговая строка байтов (машинный код).
        """
        self.bytecode = bytearray()
        for instr in instructions:
            self.encode_instruction(instr)
        return bytes(self.bytecode)
