# ------------------------------------------------------------------------
#  \\//
#   \/aporIO - Vapor GraphQL Frontend API Server
#
#
#  Author: Thomas Rampelberg (thomasr@vapor.io)
#  Date:   24 Feb 2017
# ------------------------------------------------------------------------

IMG_NAME := vaporio/graphql-frontend-x64
PKG_VER := $(shell python synse_graphql/__init__.py)
export GIT_VER := $(shell /bin/sh -c "git log --pretty=format:'%h' -n 1 || echo 'none'")

.PHONY: build
build:
	docker build -f dockerfile/release.dockerfile \
	    -t ${IMG_NAME}:latest \
	    -t ${IMG_NAME}:${PKG_VER} \
	    -t ${IMG_NAME}:${GIT_VER} .


.PHONY: test
test:
	docker-compose -f compose/test.yml up \
	    --build \
	    --abort-on-container-exit \
	    --exit-code-from synse-graphql-test


# FIXME - needs a dev composefile
#dev:
#	docker-compose -f docker-compose.yml run --rm test /bin/sh


# meant to be run from within the docker container
one:
	tox -e py36 -- $(test)
