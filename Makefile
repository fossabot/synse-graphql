#
# Synse GraphQL
#

IMG_NAME := vaporio/synse-graphql
PKG_NAME := $(shell python -c "import synse_graphql ; print(synse_graphql.__title__)")
PKG_VER := $(shell python -c "import synse_graphql ; print(synse_graphql.__version__)")
export GIT_VER := $(shell /bin/sh -c "git log --pretty=format:'%h' -n 1 || echo 'none'")

.PHONY: build
build:  ## Build the docker image for Synse GraphQL locally
	docker build -f dockerfile/base.dockerfile \
		-t ${IMG_NAME}:latest \
		-t ${IMG_NAME}:${PKG_VER} \
		-t ${IMG_NAME}:${GIT_VER} .

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


.PHONY: version
version: ## Print the version of Synse GraphQL
	@echo "$(PKG_VER)"

.PHONY: help
help:  ## Print Make usage information
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.DEFAULT_GOAL := help