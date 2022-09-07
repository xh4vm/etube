FROM python:3.10-slim AS auth-builder

WORKDIR /opt
COPY requirements.txt modules ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev gcc musl-dev libc-dev \
     && pip install --upgrade pip \
     && pip3 install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=auth-builder /opt /opt

WORKDIR /opt/restful
EXPOSE ${AUTH_APP_PORT}
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

COPY . .
RUN pip install --no-index --find-links=/opt/wheels -r requirements.txt