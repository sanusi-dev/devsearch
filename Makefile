.PHONY: install migrate run css mailer createsuperuser check

## install  : Create virtual environment and install all Python dependencies
install:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	npm install

## migrate  : Run database migrations
migrate:
	.venv/bin/python manage.py migrate

## run      : Start the Django development server
run:
	.venv/bin/python manage.py runserver

## css      : Build the Tailwind CSS bundle once
css:
	npm run build:css

## css-watch : Watch for CSS changes and rebuild automatically
css-watch:
	npm run watch:css

## mailer   : Start the background email worker (polls queue every 30s)
mailer:
	./run_mailer.sh

## notify   : Manually trigger unread-message email notifications
notify:
	.venv/bin/python manage.py notify_unread_messages

## superuser : Create an admin superuser account
superuser:
	.venv/bin/python manage.py createsuperuser

## check    : Run Django system checks
check:
	.venv/bin/python manage.py check

## help     : Show this help message
help:
	@grep -E '^##' Makefile | sed 's/## //'
