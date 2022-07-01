FROM python:3.9

RUN pip install --upgrade pip \
    && mkdir /app && mkdir /app/img_tmp
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN ~/.poetry/bin/poetry config virtualenvs.in-project true
ADD . /app


WORKDIR /app
RUN ~/.poetry/bin/poetry install

CMD .venv/bin/python main.py 