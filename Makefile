run:
	poetry run python manage.py runserver 0.0.0.0:8000

lint: mypy pylint

mypy:
	poetry run mypy .

pylint:
	poetry run pylint freva
	poetry run pylint history
