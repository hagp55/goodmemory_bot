APP_CONTAINER = django
DB_CONTAINER = postgres
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs

app:
	${DC} up --build -d

app-restart:
	${DC} restart

app-down:
	${DC} down

app-logs:
	${DC} logs --follow

app-django_logs:
	${DC} logs --follow ${APP_CONTAINER}

app-postgres_logs:
	${DC} logs --follow ${DB_CONTAINER}

app-shell:
	${DC} exec ${APP_CONTAINER} /bin/bash

app-shell_plus:
	${DC} exec ${APP_CONTAINER} python3 manage.py shell_plus

mypy:
	${DC} exec -T ${APP_CONTAINER} mypy --explicit-package-bases .

ruff-check:
	${DC} exec -T ${APP_CONTAINER} ruff check .

ruff-fix:
	${DC} exec -T ${APP_CONTAINER} ruff check . --fix
