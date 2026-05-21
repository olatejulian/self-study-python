build:
    uv build

format:
    uv run ruff format

lint:
    uv run ruff check --fix

test:
    uv run pytest --cov

typecheck:
    uv run pyright
    uv run mypy .
