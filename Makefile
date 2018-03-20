flake8:
	flake8 viesvatcheck tests

test:
	python -m pytest tests/

mypy:
	python -m mypy viesvatcheck/ --ignore-missing-imports

lint: test flake8 mypy