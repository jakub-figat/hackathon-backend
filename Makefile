build-dev:
	docker-compose build

up-dev:
	docker-compose up

format:
	docker-compose run --rm --entrypoint "" backend bash -c "isort . && black ."

bash:
	docker-compose run --rm --entrypoint "" backend bash

db-shell:
	docker-compose exec db bash -c "psql -U postgres"

alembic-revision:
	docker-compose run --rm backend bash -c "alembic revision --autogenerate -m '$(name)'"

alembic-upgrade:
	docker-compose run --rm backend bash -c "alembic upgrade head"

unit-test:
	docker-compose run --rm --entrypoint "" backend bash -c "coverage run --source=src -m pytest tests/unit"

integration-test:
	docker-compose run --rm backend bash -c "coverage run --source=src -m pytest tests/integration"

test:
	docker-compose run --rm backend bash -c "coverage run --source=src -m pytest tests"

cov-html:
	docker-compose run --rm --entrypoint "" backend bash -c "coverage html"