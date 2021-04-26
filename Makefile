MODULE_NAME := foolbox
MODULE_ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

DOCKER_IMAGE_TAG := mlsploit-module/$(MODULE_NAME)
HOST_INPUT_DIR := $(abspath $(MODULE_ROOT)/input)
HOST_OUTPUT_DIR := $(abspath $(MODULE_ROOT)/output)
DOCKER_VOLUME_ARGS := -v "$(HOST_INPUT_DIR)":/mnt/input
DOCKER_VOLUME_ARGS += -v "$(HOST_OUTPUT_DIR)":/mnt/output

.PHONY: all
all: mlsploit_module.yaml docker_image

mlsploit_module.yaml:
	python _buildmodule.py

.PHONY: docker_image
docker_image:
	docker build -t $(DOCKER_IMAGE_TAG) $(MODULE_ROOT)

.PHONY: test_docker_image
test_docker_image: docker_image
	rm -f output/output.json output/MLSPLOIT.dset.zip
	docker run $(DOCKER_VOLUME_ARGS) --rm -it $(DOCKER_IMAGE_TAG)

.PHONY: run_docker_image_shell
run_docker_image_shell: docker_image
	docker run $(DOCKER_VOLUME_ARGS) --rm -it $(DOCKER_IMAGE_TAG) bash
