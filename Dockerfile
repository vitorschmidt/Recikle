FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONNUNBUFFERED 1

COPY ./requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

WORKDIR /code

COPY . /code/