# Кинотеатр etube

[Ссылка на работу](https://github.com/xh4vm/etube-FastAPI)

## Запуск проекта (пока что без сервиса авторизации)
``` 
cp .env.example .env
cp ./backend/sqlite_to_postgres/.env.example ./backend/sqlite_to_postgres/.env
rm -rf ./backend/nginx/static && cp -r ./backend/nginx/static_defaults/ ./backend/nginx/static
make build
```

## Запуск сервиса авторизации
```
cp .env.example .env
make build-auth
make test-auth
```

## Докуметация
#### API кинотеатр
http://localhost:8000/api/openapi
#### Сервис авторизации
http://localhost:9090/doc/swagger


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
