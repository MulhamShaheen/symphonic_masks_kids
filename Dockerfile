FROM ubuntu:latest
FROM mwader/static-ffmpeg:latest
LABEL authors="mulsha"

FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update -y && apt upgrade -y
RUN apt install ffmpeg -y

WORKDIR app/
COPY kids_app/requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install ffmpeg

COPY kids_app /app/

RUN python manage.py makemigrations
RUN python manage.py migrate