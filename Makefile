#
# Synse GraphQL
#

PKG_NAME    := $(shell python -c "import synse_graphql ; print(synse_graphql.__title__)")
PKG_VERSION := $(shell python -c "import synse_graphql ; print(synse_graphql.__version__)")
IMAGE_NAME  := vaporio/synse-graphql

GIT_COMMIT ?= $(shell git rev-parse --short HEAD 2> /dev/null || true)
GIT_TAG    ?= $(shell git describe --tags 2> /dev/null || true)
BUILD_DATE := $(shell date -u +%Y-%m-%dT%T 2> /dev/null)

HAS_PY36        := $(shell which python3.6 || python -V 2>&1 | grep 3.6 || python3 -V 2>&1 | grep 3.6)
HAS_PIP_COMPILE := $(shell which pip-compile)


.PHONY: build
build:  ## Build the docker image for Synse GraphQL locally
	docker build -f dockerfile/base.dockerfile \
		--build-arg BUILD_DATE=$(BUILD_DATE) \
		--build-arg BUILD_VERSION=$(PKG_VERSION) \
		--build-arg VCS_REF=$(GIT_COMMIT) \
		-t ${IMAGE_NAME}:latest \
		-t ${IMAGE_NAME}:local \
		-t ${IMAGE_NAME}:${PKG_VERSION} .

.PHONY: test
test:  ## Run the tests for Synse GraphQL
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

.PHONY: down
down:
	docker-compose -f compose/base.yml -f compose/dev.yml down

.PHONY: logs
logs:
	docker-compose -f compose/base.yml -f compose/dev.yml logs

.PHONY: github-tag
github-tag:  ## Create and push a tag with the current version
	git tag -a ${PKG_VERSION} -m "${PKG_NAME} version ${PKG_VERSION}"
	git push -u origin ${PKG_VERSION}

.PHONY: update-deps
update-deps:  ## Update the frozen pip dependencies (requirements.txt)
ifndef HAS_PIP_COMPILE
	pip install pip-tools
endif
	pip-compile --output-file requirements.txt setup.py

.PHONY: version
version: ## Print the version of Synse GraphQL
	@echo "$(PKG_VERSION)"

.PHONY: help
help:  ## Print Make usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help


#
# CI Targets
#

.PHONY: circleci
circleci:
	docker-compose -f compose/base.yml -f compose/test.yml -f compose/test-circleci.yml up \
	  --build \
	  --abort-on-container-exit \
	  --exit-code-from graphql

.PHONY: ci-check-version
ci-check-version:
	PKG_VERSION=$(PKG_VERSION) ./bin/ci/check_version.sh

.PHONY: ci-package
ci-package:
	python setup.py sdist --formats=gztar,zip,bztar,tar
