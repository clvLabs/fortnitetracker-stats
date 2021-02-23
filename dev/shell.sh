#!/bin/bash
docker exec \
    --interactive \
    --tty \
    $1 $2 $3 $4 $5 $6 $7 $8 $9 \
    fortnitetracker-stats \
    bash
