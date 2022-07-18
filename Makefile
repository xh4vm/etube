.PHONY: interactive build services
build: collectstatic build-dockers

.PHONY: interactive run services
run:
	docker compose up

.PHONY: daemon build services
buildd: collectstatic buildd-dockers

.PHONY: start postman/newman test API
postman-test: 
	docker run --net host -v `pwd`/backend/postgres_to_es/postman/ETLTests.json:/tmp/ETLTests.json -t postman/newman_alpine33 run /tmp/ETLTests.json

.PHONY: transfer data from sqlite into postgresql
s2p: create-venv pip-install-s2p load_data_from_s2p

.PHONY: daemon run services
rund:
	docker compose up -d

.PHONY: backend-admin cli
cli-admin:
	docker exec -it backend-admin bash

.PHONY: backend-client cli
cli-client:
	docker exec -it backend-client bash

.PHONY: backend-nginx cli
cli-nginx:
	docker exec -it nginx bash

.PHONY: clean all docker images and pyc-files
clean-all: clean-pyc clean-all-dockers

.PHONY: clean docker images and pyc-files
clean: clean-pyc clean-dockers

.PHONY: run pre-commit all files
pre-commit: create-venv pip-install-pre-commit pre-commit-files

.PHONY: create venv
create-venv:
	python3 -m venv venv

.PHONY: install requirements-build to venv
pip-install-build:
	./venv/bin/pip3 install -r requirements-build.txt

.PHONY: install requirements-pre-commit to venv
pip-install-pre-commit:
	./venv/bin/pip3 install -r requirements-pre-commit.txt

.PHONY: install requirements for sqlite to postgres script
pip-install-s2p:
	./venv/bin/pip3 install -r ./backend/sqlite_to_postgres/requirements.txt

.PHONY: load data from sqlite to postgres
load_data_from_s2p:
	./venv/bin/python3 backend/sqlite_to_postgres/load_data.py

.PHONY: collect static files
collectstatic-with-venv:
	./venv/bin/python3 backend/admin/manage.py collectstatic --noinput

.PHONY: collect static files
collectstatic: create-venv pip-install-build collectstatic-with-venv

.PHONY: interactive build docker services
build-dockers:
	docker compose up --build

.PHONY: daemon build docker services
buildd-dockers:
	docker compose up -d --build

.PHONY: run pre-commit all files
pre-commit-files:
	source venv/bin/activate; ./venv/bin/pre-commit run --all-files

.PHONY: clean-pyc
clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

.PHONY: clean all docker images
clean-all-dockers:
	T=$$(docker ps -q); docker stop $$T; docker rm $$T; docker container prune -f

.PHONY: clean docker images
clean-dockers:
	T="backend-admin backend-client db swagger"; docker stop $$T; docker rm $$T; docker container prune -f


include .env
db = db
app = etl

create_schema:
	docker exec -it ${db} psql --username=${DB_USER} --dbname=${DB_NAME} -c \
	'CREATE SCHEMA IF NOT EXISTS content;'
migrate:
	docker-compose exec backend-admin ./manage.py migrate
fill_db:
	docker-compose exec backend-admin python ./sqlite_to_postgres/load_data.py
db_connect:
	docker exec -it ${db} psql --username=${DB_USER} --dbname=${DB_NAME}

app_connect:
	docker exec -it ${app} sh