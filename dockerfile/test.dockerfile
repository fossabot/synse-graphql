FROM python:3.6-alpine
MAINTAINER Thomas Rampelberg <thomasr@vapor.io>

COPY testing-requirements.txt .

RUN pip install --upgrade pip setuptools
RUN pip install -r testing-requirements.txt

WORKDIR /code

CMD ["bin/run_tests.sh"]