FROM python:3.10-slim AS auth-grpc-builder

WORKDIR /opt
COPY requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends build-essential python-dev python3-dev g++ \
     && pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/grpc
EXPOSE ${AUTH_GRPC_PORT}
ENV PYTHONPATH /opt/grpc/:/opt/grpc:/opt/grpc/messages

ENTRYPOINT ["python3", "main.py"]

COPY --from=auth-grpc-builder /usr/local /usr/local

COPY . .