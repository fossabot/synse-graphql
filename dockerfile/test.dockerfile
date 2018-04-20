FROM vaporio/synse-graphql

LABEL maintainer="vapor@vapor.io"

RUN pip install --upgrade pip setuptools tox==2.6.0

CMD ["bin/run_tests.sh"]
