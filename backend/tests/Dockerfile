FROM python:3.10-slim as test-builder

WORKDIR /opt
COPY requirements.txt ./

RUN  apt-get update && apt-get install -y --no-install-recommends gcc musl-dev libc-dev tini \
     && pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=test-builder /opt /opt
COPY --from=test-builder /usr/bin/tini /usr/bin/tini

WORKDIR /opt/tests
ENTRYPOINT [ "tini", "--" ]
CMD ["./entrypoint.sh"]

COPY . .
RUN chmod +x entrypoint.sh && pip install --no-index --find-links=/opt/wheels -r requirements.txt