#!/bin/bash

alembic upgrade head
echo "alembic upgraded"

python3 app/db/poerty.py
cho "admin is created"

python3 code/main.py