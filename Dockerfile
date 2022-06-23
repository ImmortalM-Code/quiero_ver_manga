FROM python:3.9

RUN pip install --upgrade pip \
    && mkdir /app

ADD . /app

WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN cd app && .poetry/bin/poetry install

CMD python /app/main.py
