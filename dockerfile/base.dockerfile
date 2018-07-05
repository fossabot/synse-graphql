FROM python:3.6-alpine

LABEL maintainer="vapor@vapor.io"

COPY requirements.txt /tmp/requirements.txt
RUN apk add --update --no-cache build-base \
    && pip install -r /tmp/requirements.txt \
    && apk del build-base

# Image Metadata -- http://label-schema.org/rc1/
# This is set after the dependency install so we can cache that layer
ARG BUILD_DATE
ARG BUILD_VERSION
ARG VCS_REF

LABEL org.label-schema.schema-version="1.0" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="vaporio/synse-graphql" \
      org.label-schema.vcs-url="https://github.com/vapor-ware/synse-graphql" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vendor="Vapor IO" \
      org.label-schema.version=$BUILD_VERSION

COPY . /code
WORKDIR /code

RUN python setup.py install

CMD ["python", "synse_graphql"]
