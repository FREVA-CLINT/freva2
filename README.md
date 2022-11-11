# freva2

Right now just some boilerplate..

## How to run

Assuming a mysql-db according to the values in freva/settings.py is running

```
  poetry shell
  poetry install
  poetry run python manage.py migrate
  poetry run python manage.py createsuperuser
  ...
  poetry run python runserver

```

If app is running you can reacht the Interface via `http://localhost:8000` and login as the admin user at `http://localhost:8000/admin`
After login, `http://localhost:8000/api/getjson` should become accessible
