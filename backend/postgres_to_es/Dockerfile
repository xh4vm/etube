FROM python:3.10-slim AS build 

WORKDIR /opt
COPY requirements.txt .

RUN apt-get update && apt-get install -y --no-install-recommends curl && pip install -r requirements.txt 


FROM python:3.10-slim

WORKDIR /opt/etl
ENTRYPOINT [ "/bin/bash", "-c",  "./elasticsearch/init_indices.sh && celery -A etl worker -l info -B" ]

COPY --from=build /usr/bin /usr/bin
COPY --from=build /usr/lib /usr/lib
COPY --from=build /usr/local /usr/local
COPY . .
RUN chmod +x ./elasticsearch/init_indices.sh