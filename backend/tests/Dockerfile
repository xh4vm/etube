FROM python:3.10-slim

WORKDIR /opt/tests
COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends gcc musl-dev libc-dev && \
     pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/opt/tests/entrypoint.sh"]