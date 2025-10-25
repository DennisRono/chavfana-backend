.PHONY: install dev test lint format clean migrate upgrade seed

install:
	poetry install

dev:
	poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	poetry run pytest

lint:
	poetry run flake8 .
	poetry run isort --check-only .
	poetry run black --check .

format:
	poetry run isort .
	poetry run black .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

migrate:
	poetry run alembic revision --autogenerate -m "$(msg)"

upgrade:
	poetry run alembic upgrade head

seed:
	poetry run python bin/seed.py

docker-build:
	docker build -t kenya-addresses .

docker-run:
	docker run -p 8000:8000 --env-file .env kenya-addresses
