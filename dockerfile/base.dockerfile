FROM python:3.6-alpine
MAINTAINER Thomas Rampelberg <thomasr@vapor.io>

COPY requirements.txt /tmp/requirements.txt
RUN set -e -x \
    && apk add --update --no-cache build-base \
    && pip install -r /tmp/requirements.txt \
    && apk del build-base

COPY . /code
WORKDIR /code

CMD ["python", "runserver.py"]
