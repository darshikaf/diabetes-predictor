.PHONY: build clean ecr-login run-local test-integration test-unit style-check style-inplace

DOCKER_REGISTRY   ?= hub.docker.com
DOCKER_REPO       ?= darshika/diabetes-predictor
BUILD_TAG         := latest
TS                := $(shell date "+%Y%m%d%H%M%S")
NAME              := $(lastword $(subst /, ,$(DOCKER_REPO)))

CI_REPO_URL       ?= $(shell git remote get-url origin)
CI_COMMIT         ?= $(shell git rev-parse --short HEAD)

# Use cached builds on macOS
UNAME_S := $(shell uname -s)
ifneq ($(UNAME_S),Darwin)
	DOCKER_BUILD_ARGS ?= "--no-cache"
endif


IMAGE_NAME = ${DOCKER_REPO}:${VERSION}
IMAGE_EXISTS = $(shell docker images -q ${IMAGE_NAME} 2> /dev/null)
ifeq ("${IMAGE_EXISTS}", "")
build: build-test build-app
else
clean-docker: clean-docker-app
endif

build-app:
	docker build \
		--build-arg VERSION=${VERSION} \
		-t ${IMAGE_NAME} \
		-f docker/app.Dockerfile .


build-test:
	docker build \
		--build-arg VERSION=${VERSION} \
		-f docker/test.Dockerfile .


clean-docker-base:
	docker rmi ${IMAGE_NAME}


clean-docker-app:
	docker rmi ${IMAGE_NAME} 


clean-docker:
	echo "Removed docker images"


push-docker:
	docker push ${IMAGE_NAME}

clean:
	docker-compose down
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.local.yml \
		-f docker-compose.test.yml \
		rm -f


run-local: clean
	docker-compose -f docker-compose.yml -f docker-compose.local.yml up \
    	--exit-code-from predictor  \
    	--force-recreate \
    	--always-recreate-deps


generate-migration: clean
	docker-compose -f docker-compose.yml -f docker-compose.alembic.yml up \
		--exit-code-from predictor  \
    	--force-recreate \
    	--always-recreate-deps


style-check:
	.conda/run_style.sh


style-inplace:
	.conda/run_style.sh --in-place-fixup yes


test-integration:
	.conda/run_test.sh --test-suite integration


test-unit:
	.conda/run_test.sh --test-suite unit
