FROM python:3.10-slim as test-builder

WORKDIR /opt
COPY requirements.txt ./

RUN  apt-get update && apt-get install -y --no-install-recommends gcc musl-dev libc-dev \
     && pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/tests
ENTRYPOINT ["/opt/tests/entrypoint.sh"]
COPY --from=test-builder /usr/local /usr/local

COPY . .
RUN chmod +x entrypoint.sh