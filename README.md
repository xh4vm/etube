# Кинотеатр etube

[Ссылка на работу](https://github.com/xh4vm/etube-FastAPI)

## Запуск проекта (пока что без сервиса авторизации)
``` 
cp .env.example .env
cp ./backend/sqlite_to_postgres/.env.example ./backend/sqlite_to_postgres/.env
rm -rf modules backend/auth/restful/modules backend/client/modules && mkdir modules
cd backend/auth && python3 setup.py sdist && mv dist/* ../../modules && rm -rf auth.egg-info dist && cd ../..
cd backend/jaeger && python3 setup.py sdist && mv dist/* ../../modules && rm -rf jaeger_telemetry.egg-info dist && cd ../..
cp -r ./modules backend/auth/restful && cp -r ./modules backend/client/
rm -rf ./backend/nginx/static && cp -r ./backend/nginx/static_defaults/ ./backend/nginx/static
make build
```

## Запуск сервиса авторизации
```
cp .env.example .env
cd backend/auth && python3 setup.py sdist && mv dist ../../modules && rm -rf auth.egg-info dist && cd ../..
cp -r ./modules backend/auth/restful
echo -e "\nauth @ file://`pwd`/modules/auth-0.1.0.tar.gz" | tee -a requirements-test-auth.txt 
make build-auth
make test-auth
```

## Документация
#### API кинотеатр
http://localhost:8000/api/openapi
#### Сервис авторизации
http://localhost:9090/doc/swagger
#### Cоздание суперпользователя сервиса авторизации (CLI)
```
1) make auth_connect
2) cd api
3) flask superuser create admin mail@mail.ru 123qwe
```
#### Cоздание суперпользователя сервиса авторизации (терминал)
```
make db_create_superuser
```

#### Миграции сервиса авторизации
```
backend/auth/restful/api/migrations
```

## Описание сценариев Makefile
- `make build-auth` - установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров; пересобрать контейнеры в интерактивном режиме для сервиса авторизации
- `make test-auth` - локально протестировать ручки сервиса авторизации
- `make build` - установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров; добавить статические файлы; пересобрать контейнеры в интерактивном режиме
- `make buildd` -  установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров; добавить статические файлы; пересобрать контейнеры в режиме демона
- `make build-test` - установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров;  пересобрать контейнеры для тестирования в интерактивном режиме
- `make test` - оттестировать API
- `make run` - запустить контейнеры в интерактивном режиме
- `make rund` - запустить контейнеры в режиме демона 
- `make postman-test` - запустить тесты перекаченных данных с помощью сервиса етл
- `make s2p` - запустить перекачку данных из movies_database.sqlite в постгрес. Постгрес должен быть поднят.
- `make cli-admin` - запустить консоль к контейнеру с админкой
- `make cli-client` - запустить консоль к контейнеру с апи
- `make pre-commit` - установить виртуальное окружение; установить необходимые для запуска прекоммитов зависимости; добавить статические файлы; запустить выполнение инструкций прекоммита
- `make clean-pyc` - удалить все pyc-файлы из проекта
- `make clean-all` - остановить и удалить все контейнеры и занимаемую ими память и удалить все pyc-файлы из проекта
- `make clean` - остановить и удалить контейнеры соответствующие данному проекту и занимаемую ими память и удалить все pyc-файлы из проекта
