#!/usr/bin/env zsh
# set -x

echo "== Pre-fixing Ruff linting...==========" && uv run ruff check --fix . && echo "== Pre-running Ruff formatting...==========" && uv run ruff format . && echo "== Running Ruff linter...==========" && uv run ruff check . && echo "== Checking code formatting ============" && uv run ruff format --diff . && echo "== Running type checker ============" && uv run ty check && uv run pytest 
