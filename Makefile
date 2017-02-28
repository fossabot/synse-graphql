# ------------------------------------------------------------------------
#  \\//
#   \/aporIO - Vapor GraphQL Frontend API Server
#
#
#  Author: Thomas Rampelberg (thomasr@vapor.io)
#  Date:   24 Feb 2017
# ------------------------------------------------------------------------

image := vaporio/graphql-frontend-x64

build:
	docker-compose -f graphql_frontend.yml build

# get date for tagging on push
date := $(shell /bin/date "+%m%d%y-%H%M")

dev: build
	docker-compose -f docker-compose.yml run --service-ports --rm graphql_frontend /bin/sh

test:
	docker-compose -f docker-compose.yml run --rm graphql_frontend tox

clean:
	docker-compose -f docker-compose.yml down
