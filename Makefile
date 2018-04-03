# ------------------------------------------------------------------------
#  \\//
#   \/aporIO - Vapor GraphQL Frontend API Server
#
#
#  Author: Thomas Rampelberg (thomasr@vapor.io)
#  Date:   24 Feb 2017
# ------------------------------------------------------------------------

IMG_NAME := vaporio/synse-graphql
PKG_VER := $(shell python synse_graphql/__init__.py)
export GIT_VER := $(shell /bin/sh -c "git log --pretty=format:'%h' -n 1 || echo 'none'")

.PHONY: build
build:
	docker build -f dockerfile/base.dockerfile \
		-t ${IMG_NAME}:latest \
		-t ${IMG_NAME}:${PKG_VER} \
		-t ${IMG_NAME}:${GIT_VER} .

.PHONY: test
test:
	docker-compose -f compose/base.yml -f compose/dev.yml -f compose/test.yml up \
	  --build \
	  --abort-on-container-exit \
	  --exit-code-from graphql

.PHONY: dev
dev:
	docker-compose -f compose/base.yml -f compose/dev.yml up \
		-d \
		--build
	-docker exec -it synse-graphql /bin/sh
	$(MAKE) down

.PHONY: run
run:
	docker-compose -f compose/base.yml -f compose/dev.yml -f compose/run.yml up \
		-d \
		--build

.PHONY: circleci
circleci:
	docker-compose -f compose/base.yml -f compose/test.yml -f compose/test-circleci.yml up \
	  --build \
	  --abort-on-container-exit \
	  --exit-code-from graphql

.PHONY: down
down:
	docker-compose -f compose/base.yml -f compose/dev.yml down

.PHONY: logs
logs:
	docker-compose -f compose/base.yml -f compose/dev.yml logs
