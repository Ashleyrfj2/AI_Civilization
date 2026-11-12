.PHONY: setup install test lint format run smoke determinism godot-check clean

setup: install

install:
	python3 -m pip install -e ".[dev]"

test:
	python3 -m pytest

lint:
	python3 -m ruff check backend tests
	python3 -m ruff format --check backend tests

format:
	python3 -m ruff check --fix backend tests
	python3 -m ruff format backend tests

run:
	python3 -m ai_civilization.cli run --ticks 5

smoke:
	python3 -m pytest tests/smoke -q

determinism:
	bash scripts/check_determinism.sh

godot-check:
	bash scripts/check_godot.sh

clean:
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov dist build
	find backend tests -type d -name __pycache__ -prune -exec rm -rf {} +
