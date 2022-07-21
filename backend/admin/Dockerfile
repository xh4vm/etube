FROM python:3.10-slim AS admin-build

WORKDIR /opt
COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev \
     && pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/app
EXPOSE ${ADMIN_APP_PORT}
ENTRYPOINT ["uwsgi", "--strict", "--ini", "uwsgi.ini"]

COPY --from=admin-build /usr/local /usr/local
RUN  mkdir -p /var/www/static/

COPY . .