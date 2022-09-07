FROM python:3.10-slim AS client-builder

WORKDIR /opt
COPY requirements.txt modules ./

RUN apt-get update && apt-get install -y --no-install-recommends gcc musl-dev libc-dev && \
     pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=client-builder /opt /opt

WORKDIR /opt/content
ENTRYPOINT ["/bin/bash", "-c", "chmod +x ./start.sh && ./start.sh"]

COPY . .
RUN pip install --no-index --find-links=/opt/wheels -r requirements.txt