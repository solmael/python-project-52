install:
	uv sync
migrate:
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