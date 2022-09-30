build-dev:
	docker-compose build

up-dev:
	docker-compose up

format:
	docker-compose run --rm --entrypoint "" backend bash -c "isort . && black ."

bash:
	docker-compose run --rm --entrypoint "" backend bash

db-shell:
	docker-compose exec postgres bash -c "psql -U postgres hackathon"

alembic-revision:
	docker-compose run --rm backend bash -c "alembic revision --autogenerate -m '$(name)'"

alembic-upgrade:
	docker-compose run --rm backend bash -c "alembic upgrade head"

test:
	docker-compose run --rm backend bash -c "pytest"

integration-test:
	docker-compose run --rm backend bash -c "pytest --integration"


cov-html:
	docker-compose run --rm --entrypoint "" backend bash -c "coverage html"
