FROM python:3.10-slim AS auth-grpc-builder

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev g++ \
     && pip install --upgrade pip \
     && pip install wheel && pip3 wheel -r requirements.txt --wheel-dir=/opt/wheels


FROM python:3.10-slim

COPY --from=auth-grpc-builder /opt /opt

WORKDIR /opt/grpc
EXPOSE ${AUTH_GRPC_PORT}
ENV PYTHONPATH /opt/grpc/:/opt/grpc:/opt/grpc/messages

ENTRYPOINT ["python3", "main.py"]

COPY . .
RUN pip install --no-index --find-links=/opt/wheels -r requirements.txt