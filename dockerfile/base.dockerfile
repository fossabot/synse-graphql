FROM python:3.6-alpine

LABEL maintainer="vapor@vapor.io"

COPY requirements.txt /tmp/requirements.txt
RUN apk add --update --no-cache build-base \
    && pip install -r /tmp/requirements.txt \
    && apk del build-base

COPY . /code
WORKDIR /code

CMD ["python", "synse_graphql"]
