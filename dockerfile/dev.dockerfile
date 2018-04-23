FROM vaporio/synse-graphql

LABEL maintainer="vapor@vapor.io"

RUN apk add --no-cache \
  build-base \
  curl

RUN pip install --upgrade \
  pip \
  setuptools \
  tox

CMD ["bin/sleep.sh"]
