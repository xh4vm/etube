FROM python:3.10-slim AS client-build

WORKDIR /opt
COPY requirements.txt ./

RUN pip install --upgrade "pip>=22.1" \
     && pip install -r requirements.txt


FROM python:3.10-slim

WORKDIR /opt/app
ENTRYPOINT ["/bin/bash", "-c", "chmod +x ./start.sh && ./start.sh"]

COPY --from=client-build /usr/local /usr/local

COPY . .