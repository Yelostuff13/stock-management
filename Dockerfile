FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql \
    && apk add postgresql-dev \
    && apk add --no-cache postgresql-libs \
    && apk add jpeg-dev zlib-dev libjpeg \
    && python3 -m pip install -r requirements.txt --no-cache-dir \
    && apk del build-deps 

COPY . .
