install:
	uv sync
migrate:
	python manage.py makemigrations task_manager
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check .

fix:
	uv run ruff check . --fix

env:
	source .venv/bin/activate

dev:
	uv run manage.py runserver

compilemessages:
	uv run django-admin compilemessages

test:
	python manage.py test task_manager --verbosity=2

test-coverage:
	coverage run --source=task_manager manage.py test task_manager
	coverage xml --rcfile=.coveragerc