#!/usr/bin/env bash

MODULENAME="foolbox"

docker build -t ${MODULENAME} .

yes | rm -f output/MLSPLOIT.db

docker run \
    -v "$(pwd)/input":/mnt/input \
    -v "$(pwd)/output":/mnt/output \
    --rm -it ${MODULENAME}
