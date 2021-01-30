#!/bin/bash
docker build \
    -t fortnitetracker-stats \
    --progress=plain \
    --force-rm \
    $1 $2 $3 $4 \
    .
