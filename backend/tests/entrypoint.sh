#!/bin/bash

python3 -m functional.utils.wait_for_es &&
python3 -m functional.utils.wait_for_redis &&
pytest functional/src
