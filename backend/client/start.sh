#!/bin/bash 

uvicorn src.main:app --host 0.0.0.0 --port $CLIENT_APP_PORT