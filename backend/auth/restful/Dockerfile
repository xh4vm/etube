FROM python:3.10-slim AS auth-builder

WORKDIR /opt
COPY requirements.txt modules/ ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev \
     && pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/app
EXPOSE ${AUTH_APP_PORT}
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

COPY --from=auth-builder /usr/local /usr/local

COPY . .