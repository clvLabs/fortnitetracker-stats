#!/bin/bash
docker build \
    -t fortnitetracker-stats \
    --progress=plain \
    --force-rm \
    $1 $2 $3 $4 $5 $6 $7 $8 $9 \
    .
