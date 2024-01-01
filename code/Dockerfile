FROM python:3.10

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code/app:/code/app/api"


COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .


RUN chmod a+x docker/app.sh


CMD alembic upgrade head && python3 app/db/poerty.py && uvicorn app.main:app --host "0.0.0.0" --port 8000 --workers 4 --reload




