
lint: mypy pylint

mypy:
	poetry run mypy .

pylint:
	poetry run pylint freva
	poetry run pylint history
