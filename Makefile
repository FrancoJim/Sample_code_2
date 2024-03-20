.PHONY: run install build test clean

run:
	poetry install --no-dev
	poetry run python3 sample_1/main.py

install:
	poetry install --no-dev
	
build:
	poetry build

test:
	poetry run pytest

clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete