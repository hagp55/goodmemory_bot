API_SERVICE = django
DB_SERVICE = postgres
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

up:
	${DC} up --build -d

restart:
	${DC} restart

down:
	${DC} down

logs:
	${DC} logs --follow

django_logs:
	${DC} logs --follow ${API_SERVICE}

postgres_logs:
	${DC} logs --follow ${DB_SERVICE}

shell:
	${DC} exec ${API_SERVICE} /bin/bash

shell_plus:
	${DC} exec ${API_SERVICE} python3 manage.py shell_plus

makemigrations:
	${DC} exec -T ${API_SERVICE} python3 manage.py makemigrations

migrate:
	${DC} exec -T ${API_SERVICE} python3 manage.py migrate

mypy:
	${DC} exec -T ${API_SERVICE} mypy --explicit-package-bases .

tests:
	${DC} exec -T ${API_SERVICE} pytest -vs

tests-coverage:
	${DC} exec ${API_SERVICE} pytest --cov=. .

tests-coverage-generate-report:
	${DC} exec ${API_SERVICE} pytest --cov=. --cov-report=html --cov-report=term


ruff-check:
	${DC} exec -T ${API_SERVICE} ruff check .

ruff-fix:
	${DC} exec -T ${API_SERVICE} ruff check . --fix
