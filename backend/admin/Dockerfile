FROM python:3.10-slim AS admin-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev gcc musl-dev libc-dev \
     && pip install --upgrade pip \
     && pip3 install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=admin-builder /opt /opt

WORKDIR /opt/admin
EXPOSE ${ADMIN_APP_PORT}
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

COPY . .
RUN  mkdir -p /var/www/static/ && pip install --no-index --find-links=/opt/wheels -r requirements.txt