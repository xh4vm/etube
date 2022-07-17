# etube-FastAPI. Проектная работа 4 спринта

[Ссылка на работу](https://github.com/xh4vm/etube-FastAPI)

## Запуск проекта
1) cd 01_etl
2) cp .env.example .env
3) make build

## Описание сценариев Makefile
- `make build` - установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров; добавить статические файлы; пересобрать контейнеры в интерактивном режиме
- `make buildd` -  установить виртуальное окружение; установить необходимые зависимости для запуска контейнеров; добавить статические файлы; пересобрать контейнеры в режиме демона
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
