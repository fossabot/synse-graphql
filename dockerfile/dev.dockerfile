FROM vaporio/synse-graphql
MAINTAINER Thomas Rampelberg <thomasr@vapor.io>

RUN apk add --no-cache \
  build-base \
  curl

RUN pip install --upgrade \
  pip \
  setuptools \
  tox

CMD ["bin/sleep.sh"]
