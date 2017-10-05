FROM vaporio/synse-graphql
MAINTAINER Thomas Rampelberg <thomasr@vapor.io>

COPY testing-requirements.txt .

RUN pip install --upgrade pip setuptools
RUN pip install -r testing-requirements.txt

CMD ["bin/run_tests.sh"]
