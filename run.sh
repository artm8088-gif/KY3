#!/usr/bin/env bash
cd "$(dirname "$0")" || exit 1
if [ -d ".venv" ]; then
    .venv/bin/python -m src.main "$@"
else
    python3 -m src.main "$@"
fi