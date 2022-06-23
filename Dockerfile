FROM python:3.9

RUN pip install --upgrade pip \
    && mkdir /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ADD . /app
RUN cd app && ~/.poetry/bin/poetry install

WORKDIR /app

CMD .venv/bin/python /app/main.py
