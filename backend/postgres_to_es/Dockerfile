FROM python:3.10-slim AS etl-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=etl-builder /opt /opt

WORKDIR /opt/etl
ENTRYPOINT [ "celery", "-A", "etl", "worker", "-l", "info", "-B" ]

COPY . .
RUN  pip install --no-index --find-links=/opt/wheels -r requirements.txt