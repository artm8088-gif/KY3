# Makefile для проекта УВМ (Вариант №2) — Этапы 1 и 2

.PHONY: help install test lint format run run-test clean

# Переменные для удобства
PYTHON = python3
SRC_DIR = src
ASM_FILE = examples/test_program.asm
BIN_FILE = output.bin

help:
	@echo "Доступные команды:"
	@echo "  make install    - Установить зависимости (включая dev)"
	@echo "  make test       - Запустить тесты pytest"
	@echo "  make lint       - Проверить код линтером Ruff"
	@echo "  make format     - Автоформатирование кода через Ruff"
	@echo "  make run        - Запустить ассемблер (обычный режим)"
	@echo "  make run-test   - Запустить ассемблер в режиме тестирования (вывод IR + байтов)"
	@echo "  make clean      - Удалить временные файлы и кэш"

install:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest -v tests/

lint:
	ruff check .

format:
	ruff format .
	ruff check --fix .

# Обычный запуск: только создание бинарного файла
run:
	$(PYTHON) -m $(SRC_DIR).main -i $(ASM_FILE) -o $(BIN_FILE)
	@echo "Бинарный файл $(BIN_FILE) успешно создан."

# Запуск в режиме тестирования: вывод IR и байтов на экран
run-test:
	$(PYTHON) -m $(SRC_DIR).main -i $(ASM_FILE) -o $(BIN_FILE) -t

clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f $(BIN_FILE)