FROM python:3.10-slim AS etl-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl && pip install -r requirements.txt 


FROM python:3.10-slim

WORKDIR /opt/es_initer
ENTRYPOINT [ "python3", "./src/main.py" ]

COPY --from=etl-builder /usr/bin /usr/bin
COPY --from=etl-builder /usr/lib /usr/lib
COPY --from=etl-builder /usr/local /usr/local
COPY ./src ./src